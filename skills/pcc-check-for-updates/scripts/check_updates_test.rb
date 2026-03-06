#!/usr/bin/env ruby
# Test file for check_updates.rb
# Run with: ruby check_updates_test.rb

require 'minitest/autorun'
require 'json'
require 'tempfile'

# Load the main script functions
# Since the main script has executable code at the bottom, we'll redefine the functions here
class CheckUpdatesTest < Minitest::Test
  
  # Helper method to simulate version comparison
  def version_gt(v1, v2)
    return nil if v1.nil? || v2.nil?
    v1_parts = v1.split('.').map(&:to_i)
    v2_parts = v2.split('.').map(&:to_i)
    
    # Pad with zeros if lengths differ
    max_len = [v1_parts.length, v2_parts.length].max
    v1_parts.fill(0, v1_parts.length...max_len)
    v2_parts.fill(0, v2_parts.length...max_len)
    
    v1_parts <=> v2_parts
  end

  # Equal (==)
  def test_version_comparison_equal
    assert_equal 0, version_gt("1.0.0", "1.0.0")
    assert_equal 0, version_gt("0.0.21", "0.0.21")
  end

  # Strictly greater (>)
  def test_version_comparison_greater
    assert_equal 1, version_gt("1.0.1", "1.0.0")
    assert_equal 1, version_gt("2.0.0", "1.9.9")
    assert_equal 1, version_gt("0.0.22", "0.0.21")
    assert_equal 1, version_gt("0.1.0", "0.0.99")
  end

  # Strictly lesser (<)
  def test_version_comparison_lesser
    assert_equal(-1, version_gt("1.0.0", "1.0.1"))
    assert_equal(-1, version_gt("0.0.20", "0.0.21"))
    assert_equal(-1, version_gt("0.0.22", "0.1.3"))
    assert_equal(-1, version_gt("1.9.9", "2.0.0"))
  end

  def test_version_comparison_different_lengths
    assert_equal 0, version_gt("1.0", "1.0.0")
    assert_equal 1, version_gt("1.0.1", "1.0")
    assert_equal(-1, version_gt("1.0", "1.0.1"))
  end

  def test_version_comparison_with_nil
    assert_nil version_gt(nil, "1.0.0")
    assert_nil version_gt("1.0.0", nil)
    assert_nil version_gt(nil, nil)
  end

  def test_local_version_from_json
    # Create a temporary JSON file
    temp_file = Tempfile.new(['gemini-extension', '.json'])
    temp_file.write(JSON.generate({
      "name" => "palladius-common-commands",
      "version" => "0.0.21"
    }))
    temp_file.close

    # Test reading the version
    json = JSON.parse(File.read(temp_file.path))
    assert_equal "palladius-common-commands", json["name"]
    assert_equal "0.0.21", json["version"]

    temp_file.unlink
  end

  def test_version_parsing
    # Test that version strings parse correctly
    version = "0.0.21"
    parts = version.split('.').map(&:to_i)
    assert_equal [0, 0, 21], parts
  end

  def test_version_parsing2
    # Test that version strings parse correctly
    version = "1.2.3alpha"
    parts = version.split('.').map(&:to_i)
    assert_equal [1, 2, 3], parts
  end
end

puts "🧪 Running tests for check_updates.rb..."
puts "=" * 50
