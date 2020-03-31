#!/usr/share/rvm/rubies/ruby-2.6.0/bin/ruby
require 'json'
require 'csv'

File.open(File.basename(ARGV[0]).gsub(/\.csv/, '') + '.json', 'w') {|io|
  io.puts CSV.parse(File.read(ARGV[0])).to_json
}
