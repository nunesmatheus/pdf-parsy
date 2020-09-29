# frozen_string_literal: true

class TextFromPdfService < ApplicationService
  attr_accessor :pdf_path

  RIGHT_COLUMN_SINGLE_REGEX = /\n {30,}\S/.freeze
  COLUMN_REGEX = / {5,}\S/.freeze

  def initialize(pdf_path)
    @pdf_path = pdf_path
    @split_positions = {}
  end

  def call
    text = pdf_pages.each_with_index.map do |page, page_index|
      columns = { left: [], right: [] }
      split_positions = split_positions(page, page_index)
      columns = columns_from_split(columns, page, split_positions)
      columns[:left] + columns[:right]
    end
    sanitize(text.flatten.join("\n"))
  end

  private

  def sanitize(text)
    text.
      gsub(/ +$/, '').
      gsub(/^ +/, '').
      gsub(/([a-zA-Z])-$\n([a-zA-Z])/, '\1\2').
      gsub(/([a-zA-Z[:alpha:]]) +\n/, '\1 ').
      gsub(/([a-zA-Z[:alpha:]])\n([a-zA-Z[:alpha:]])/, '\1 \2').
      gsub(/([a-zA-Z[:alpha:]])\n+([a-zA-Z[:alpha:]])/, '\1 \2').
      gsub(/,\n(a-zA-Z)/, ', \1').
      gsub(/\n{2,}/, "\n\n")
  end

  def columns_from_split(columns, page, split_positions)
    lines = page.split("\n")
    lines.each_with_index.map do |line, i|
      split_position = split_positions[:positions][i]
      if split_position
        gaps = line.scan(COLUMN_REGEX).map { |match| line.index(match) + match.size - 1 }
        new_split_position = gaps.min_by { |gap| (split_positions[:median] - gap).abs }
        columns[:left] << line[0..new_split_position - 1]
        columns[:right] << line[new_split_position..-1]
      else
        columns[:left] << line
      end
    end
    columns
  end

  def split_positions(content, page)
    @split_positions[page] ||= begin
      split_positions = []
      lines = content.split("\n")
      lines.each { |line| split_positions << split_position(line) }
      present = split_positions.reject(&:nil?)

      {
        positions: split_positions,
        average: present.sum / split_positions.size,
        median: present.sort[present.size / 2]
      }
    end
  end

  def split_position(line)
    return if single_column?(line) && left_column?(line)

    match = line.match(COLUMN_REGEX)
    return if match.blank?

    line.index(match[0]) + match[0].length - 1
  end

  def single_column?(line)
    line.match(/\A +[\S ]+/) && !line.match(/\A +[\S ]+ #{COLUMN_REGEX}/)
  end

  def left_column?(line)
    !right_column?(line)
  end

  def right_column?(line)
    !!line.match(RIGHT_COLUMN_SINGLE_REGEX)
  end

  def total_pages
    @total_pages ||= Pdftotext.pages(pdf_path).size
  end

  def pdf_pages
    @pdf_pages ||= begin
      total_pages.times.map do |page|
        Pdftotext.text(pdf_path, f: page + 1, l: page + 1)
      end
    end
  end
end
