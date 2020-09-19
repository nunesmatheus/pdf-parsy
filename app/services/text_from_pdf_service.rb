# frozen_string_literal: true

class TextFromPdfService < ApplicationService
  attr_accessor :pdf_path

  COLUMN_REGEX = / {5,}\S/.freeze

  def initialize(pdf_path)
    @pdf_path = pdf_path
    @split_positions = {}
  end

  def call
    pdf_pages.each_with_index.map do |page, page_index|
      columns = { left: [], right: [] }
      lines = page.split("\n")
      split_positions = split_positions(page, page_index)
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

      columns[:left].join("\n") + columns[:right].join("\n")
    end.join("\n\n")
  end

  private

  def split_positions(content, page)
    @split_positions[page] ||= begin
      split_positions = []
      lines = content.split("\n")
      lines.each do |line|
        split_position = nil
        match = line.match(COLUMN_REGEX)
        if match
          split_position = line.index(match[0]) + match[0].length - 1
        end
        split_positions << split_position
      end

      present = split_positions.reject(&:nil?)

      {
        positions: split_positions,
        average: present.sum / split_positions.size,
        median: present.sort[present.size / 2]
      }
    end
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
