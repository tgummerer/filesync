CC = g++

BIN = filesync 
OBJS = client.o ini.o
CFLAGS = 

$(BIN): $(OBJS)
	$(CC) -o $(BIN) $(OBJS)

client.o: client.cc

ini.o: ini.cc ini.h

clean:
	rm $(BIN) $(OBJS)
