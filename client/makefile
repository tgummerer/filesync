CC = g++

BIN = filesync 
OBJS = client.o ini.o
CFLAGS = 

$(BIN): $(OBJS)
	$(CC) -o $(BIN) $(OBJS)

client.o: client.cpp

ini.o: ini.cpp ini.h

clean:
	rm $(BIN) $(OBJS)
