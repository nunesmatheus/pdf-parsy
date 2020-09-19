# frozen_string_literal: true

require 'swagger_helper'

RSpec.describe PdfToTextController do
  describe '#create' do
    path '/pdf_to_text' do
      parameter name: :file, in: :formData, type: :file, format: :binary, required: true

      context 'when pdf does not have columns' do
        post('successful') do
          produces 'multipart/form-data'
          consumes 'multipart/form-data'
          tags 'PdfToText'

          before do
            allow(TextFromPdfService).to receive(:call).and_call_original
          end

          response(200, 'successful') do
            let(:file) do
              Rack::Test::UploadedFile.new(Rails.root.join('spec/fixtures/files/UFPR-2015.pdf'))
            end

            run_test! do
              expect(json_body[:text]).to include 'O Brasil apresenta uma situação confortável'
              expect(TextFromPdfService).to have_received(:call)
            end
          end
        end
      end
    end
  end
end
