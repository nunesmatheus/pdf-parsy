FROM ruby:2.4.6

EXPOSE 3000

RUN mkdir /pdf-parsy
WORKDIR /pdf-parsy
COPY . /pdf-parsy

RUN gem install bundler
RUN bundle install --path=vendor/bundle

CMD ["bundle", "exec", "rails", "s", "-b", "0.0.0.0"]
