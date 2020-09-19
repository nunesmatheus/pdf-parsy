Rails.application.routes.draw do
  mount Rswag::Ui::Engine => '/api-docs'
  mount Rswag::Api::Engine => '/api-docs'
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html

  resource :pdf_to_text, only: :create, controller: :pdf_to_text
  resource :pdf_images, only: :create
end
