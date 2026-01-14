#!/usr/bin/env ruby
# frozen_string_literal: true

# Cloud Build Correlation Script
# 
# This script helps correlate git commits with Cloud Build failures by comparing timestamps.
# It fetches recent git commits and Cloud Build history, then attempts to match them.
#
# Usage:
#   ruby correlate_builds.rb [PROJECT_ID]
#
# Requirements:
#   - gcloud CLI configured and authenticated
#   - git repository
#   - PROJECT_ID as argument or GCP_PROJECT env var

require 'json'
require 'time'
require 'open3'

class CloudBuildCorrelator
  def initialize(project_id)
    @project_id = project_id
    @git_commits = []
    @cloud_builds = []
  end

  def run
    puts "🔍 Cloud Build Correlation Tool"
    puts "=" * 50
    
    fetch_git_commits
    fetch_cloud_builds
    correlate
  end

  private

  def fetch_git_commits
    puts "\n📝 Fetching recent git commits..."
    cmd = "git log --pretty=format:'%H|%ai|%s|%an' --date=iso -n 20"
    output, status = Open3.capture2(cmd)
    
    unless status.success?
      puts "❌ Error fetching git commits"
      exit 1
    end

    output.each_line do |line|
      hash, date, subject, author = line.strip.split('|', 4)
      @git_commits << {
        hash: hash[0..7],
        full_hash: hash,
        time: Time.parse(date),
        subject: subject,
        author: author
      }
    end

    puts "   Found #{@git_commits.size} commits"
  end

  def fetch_cloud_builds
    puts "\n☁️  Fetching Cloud Build history..."
    cmd = "gcloud builds list --project=#{@project_id} --limit=20 --format=json"
    output, status = Open3.capture2(cmd)
    
    unless status.success?
      puts "❌ Error fetching Cloud Builds"
      puts "   Make sure PROJECT_ID is correct and you're authenticated"
      exit 1
    end

    builds = JSON.parse(output)
    @cloud_builds = builds.map do |build|
      {
        id: build['id'],
        status: build['status'],
        create_time: Time.parse(build['createTime']),
        duration: build['timing'] ? build['timing']['BUILD']&.dig('endTime') : nil
      }
    end

    puts "   Found #{@cloud_builds.size} builds"
  end

  def correlate
    puts "\n🔗 Correlation Analysis"
    puts "=" * 50
    
    first_failure = @cloud_builds.find { |b| b[:status] != 'SUCCESS' }
    
    if first_failure.nil?
      puts "✅ No failed builds found! All builds are successful."
      return
    end

    puts "\n🚨 First Failed Build:"
    puts "   ID: #{first_failure[:id]}"
    puts "   Status: #{first_failure[:status]}"
    puts "   Time: #{first_failure[:create_time]}"
    
    # Find commits around the failure time (within 10 minutes)
    time_window = 600 # 10 minutes in seconds
    suspects = @git_commits.select do |commit|
      (commit[:time] - first_failure[:create_time]).abs < time_window
    end

    if suspects.empty?
      puts "\n⚠️  No commits found within 10 minutes of the failed build"
      puts "   The failure might be infrastructure-related"
    else
      puts "\n🎯 Suspect Commits (within 10 minutes):"
      suspects.each do |commit|
        time_diff = ((commit[:time] - first_failure[:create_time]) / 60).round
        puts "\n   #{commit[:hash]} - #{time_diff}min #{time_diff > 0 ? 'after' : 'before'} build"
        puts "   #{commit[:subject]}"
        puts "   by #{commit[:author]}"
      end
      
      puts "\n💡 Suggested Actions:"
      puts "   1. Examine build logs: just cloud-build-show-log #{first_failure[:id]}"
      puts "   2. Check commit diff: git show #{suspects.first[:hash]}"
      puts "   3. File GitHub issue: [failed Cloud Build] #{first_failure[:id]} <description>"
    end
  end
end

# Main execution
if ARGV.empty? && ENV['GCP_PROJECT'].nil?
  puts "Usage: #{$0} PROJECT_ID"
  puts "   or set GCP_PROJECT environment variable"
  exit 1
end

project_id = ARGV[0] || ENV['GCP_PROJECT']
correlator = CloudBuildCorrelator.new(project_id)
correlator.run
