FROM node:lts-slim
WORKDIR /app
COPY package*.json ./
#RUN npm install
RUN rm -rf node_modules package-lock.json && npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev"]


