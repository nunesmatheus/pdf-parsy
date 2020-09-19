# frozen_string_literal: true

class PdfToTextController < ApplicationController
  def create
    render json: { text: TextFromPdfService.call(params[:file].path) }
  end
end
