import zmq
with zmq.Context() as context:
    with context.socket(zmq.REP) as socket:
        socket.bind("tcp://*:42069")

        while True:
            message = socket.recv()  # blocking call
            print(f"Received request: {message}")

            # print(type(message))
            if message == b"quit" or message == b"exit":
                break
            # time.sleep(2)

            socket.send_string(f"Server Response you sent {message}")
