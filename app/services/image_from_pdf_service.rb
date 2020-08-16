class ImagesFromPdfService < ApplicationService
  attr_accessor :pdf_path

  def initialize(pdf_path)
    @pdf_path = pdf_path
  end

  def call
    FileUtils.mkdir_p BASE_DIR
    `pdfimages -png #{pdf_path} .`

    images = []
    Dir[".*.png"].each do |file|
      images << Base64.encode64(File.read(file))
      File.delete(file)
    end

    images
  end
end
