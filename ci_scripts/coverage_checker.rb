# frozen_string_literal: true

require 'json'

coverage = JSON.parse(File.read('public/coverage/coverage.json'))

missing_coverage = []
Dir.glob('**/*.rb').each do |file|
  file_coverage = coverage['files'].find { |f| f['filename'] =~ /#{file}\Z/ }
  next if !file_coverage || (file_coverage['covered_percent'] == 100)

  missing_coverage << [file, file_coverage['covered_percent']]
end

if missing_coverage.flatten.any?
  puts missing_coverage.map { |file| "#{file[0]} tem #{file[1].round(2)}% de coverage" }.join(' | ')
else
  puts '100% de coverage!'
end
