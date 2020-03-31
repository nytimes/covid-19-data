#!/usr/bin/env ruby
require 'json'
require 'csv'

File.open(File.basename(ARGV[0]).gsub(/\.csv/, '') + '.json', 'w') {|io|
  io.puts CSV.parse(File.read(ARGV[0])).to_json
}
