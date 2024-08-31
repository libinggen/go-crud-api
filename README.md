# go-crud-api
```
brew install postgresql
brew services start postgresql
psql postgres
CREATE DATABASE yourdbname;
\c yourdbname
CREATE TABLE books (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    year VARCHAR(4)
);
\d books
INSERT INTO books (id, title, author, year) VALUES
('1', 'Book One', 'Author One', '2023'),
('2', 'Book Two', 'Author Two', '2024');
\q

mkdir go-crud-api
cd go-crud-api
go mod init go-crud-api
go get -u github.com/gorilla/mux
go get -u github.com/lib/pq
go run main.go

curl -X GET http://localhost:8000/books
curl -X GET http://localhost:8000/books/1
curl -X POST http://localhost:8000/books -H "Content-Type: application/json" -d '{"id":"3", "title":"Book Three", "author":"Author Three", "year":"2025"}'
curl -X PUT http://localhost:8000/books/3 -H "Content-Type: application/json" -d '{"title":"Updated Book Three", "author":"Updated Author Three", "year":"2026"}'
curl -X DELETE http://localhost:8000/books/3
```
