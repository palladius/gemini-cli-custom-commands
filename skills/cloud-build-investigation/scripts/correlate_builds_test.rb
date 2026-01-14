#!/usr/bin/env ruby
# frozen_string_literal: true

# Test script for correlate_builds.rb
# 
# This is a simple smoke test to ensure the script has valid syntax
# and can handle basic error cases.
#
# Usage:
#   ruby correlate_builds_test.rb

require 'open3'

class CorrelateBuildsTester
  def initialize
    @script_path = File.join(__dir__, 'correlate_builds.rb')
    @passed = 0
    @failed = 0
  end

  def run
    puts "🧪 Testing correlate_builds.rb"
    puts "=" * 50
    
    test_script_exists
    test_script_executable
    test_missing_project_id
    test_help_message
    
    puts "\n" + "=" * 50
    puts "Results: #{@passed} passed, #{@failed} failed"
    exit(@failed > 0 ? 1 : 0)
  end

  private

  def test_script_exists
    print "Test: Script file exists... "
    if File.exist?(@script_path)
      pass
    else
      fail("Script not found at #{@script_path}")
    end
  end

  def test_script_executable
    print "Test: Script is executable... "
    if File.executable?(@script_path)
      pass
    else
      fail("Script is not executable. Run: chmod +x #{@script_path}")
    end
  end

  def test_missing_project_id
    print "Test: Handles missing PROJECT_ID... "
    output, status = Open3.capture2e("ruby #{@script_path}")
    
    if status.exitstatus == 1 && output.include?("Usage:")
      pass
    else
      fail("Should exit with error when PROJECT_ID is missing")
    end
  end

  def test_help_message
    print "Test: Shows usage message... "
    output, _status = Open3.capture2e("ruby #{@script_path}")
    
    if output.include?("PROJECT_ID") || output.include?("GCP_PROJECT")
      pass
    else
      fail("Usage message should mention PROJECT_ID or GCP_PROJECT")
    end
  end

  def pass
    puts "✅ PASS"
    @passed += 1
  end

  def fail(message)
    puts "❌ FAIL"
    puts "   #{message}"
    @failed += 1
  end
end

# Run tests
tester = CorrelateBuildsTester.new
tester.run
