class PdfToTextController < ApplicationController
  def create
    images = ImagesFromPdfService.call(params[:file].path)
    render json: { images: images }
  end
end