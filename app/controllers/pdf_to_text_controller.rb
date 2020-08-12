class PdfToTextController < ApplicationController
  def create
    render json: { text: Pdftotext.text(params[:file].path) }
  end
end
