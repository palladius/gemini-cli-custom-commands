#!/usr/bin/env ruby
require 'json'
require 'open-uri'

EXTENSION_NAME = "palladius-common-commands"
REMOTE_URL = "https://raw.githubusercontent.com/palladius/gemini-cli-custom-commands/refs/heads/main/gemini-extension.json"

def get_local_version
  # Try to get it from gemini extensions list
  output = `gemini extensions list 2>/dev/null`
  
  if $?.success?
    match = output.match(/#{EXTENSION_NAME}\s+\(([^)]+)\)/)
    return match[1] if match
  end
  
  # Fallback: check if we are in the repo and have a local json
  if File.exist?("gemini-extension.json")
    begin
      json = JSON.parse(File.read("gemini-extension.json"))
      return json["version"] if json["name"] == EXTENSION_NAME
    rescue
      nil
    end
  end
  
  nil
end

def get_remote_version
  begin
    content = URI.open(REMOTE_URL).read
    json = JSON.parse(content)
    return json["version"]
  rescue => e
    puts "Error fetching remote version: #{e.message}"
    return nil
  end
end

def version_gt(v1, v2)
  return false if v1.nil? || v2.nil?
  v1_parts = v1.split('.').map(&:to_i)
  v2_parts = v2.split('.').map(&:to_i)
  
  # Pad with zeros if lengths differ
  max_len = [v1_parts.length, v2_parts.length].max
  v1_parts.fill(0, v1_parts.length...max_len)
  v2_parts.fill(0, v2_parts.length...max_len)
  
  v1_parts <=> v2_parts
end

local_ver = get_local_version
remote_ver = get_remote_version

if local_ver.nil?
  puts "Could not determine local version. Is the extension installed?"
  exit 1
end

if remote_ver.nil?
  puts "Could not determine remote version."
  exit 1
end

puts "Local version:  #{local_ver}"
puts "Remote version: #{remote_ver}"

comparison = version_gt(remote_ver, local_ver)

if comparison == 1
  puts "\n🚀 Update available!"
  puts "Run: gemini extensions update #{EXTENSION_NAME}"
elsif comparison == 0
  puts "\n✅ You are up to date."
else
  puts "\n⚠️  Your version is ahead of remote (Dev mode?)"
end
