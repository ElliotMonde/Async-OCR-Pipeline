FROM node:22-alpine

WORKDIR /app

COPY ./ocr-frontend/package*.json ./

RUN npm install

COPY ./ocr-frontend/ .

EXPOSE 5173

CMD ["npm", "run", "dev"]