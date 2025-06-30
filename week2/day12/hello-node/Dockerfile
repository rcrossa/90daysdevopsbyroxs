FROM node:22-alpine
WORKDIR /app
COPY package.json ./
COPY index.js ./
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]