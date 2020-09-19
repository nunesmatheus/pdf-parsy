# frozen_string_literal: true

class PdfImagesController < ApplicationController
  def create
    images = ImagesFromPdfService.call(params[:file].path)
    render json: { images: images }
  end
end
