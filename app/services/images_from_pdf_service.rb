# frozen_string_literal: true

class ImagesFromPdfService < ApplicationService
  attr_accessor :pdf_path

  def initialize(pdf_path)
    @pdf_path = pdf_path
  end

  def call
    `pdfimages -png #{pdf_path} #{images_hash}-`

    images = []
    Dir["#{images_hash}*"].sort.each do |file|
      images << Base64.encode64(File.read(file))
      File.delete(file)
    end

    images
  end

  private

  def images_hash
    @images_hash ||= SecureRandom.hex
  end
end
