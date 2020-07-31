import asyncio
metrix_storage = dict()


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        try:
            #chunks = data.decode('utf-8').replace('\n', '').split(' ')
            #print(chunks)
            command = self._validate(
                data.decode('utf-8').replace('\n', '')).encode('utf-8')

        except AttributeError:
            command = 'error\nwrong command\n\n'.encode('utf-8')

        self.transport.write(command)
        # 'put palm.cpu 23.7 1150864247 34\n'

    def _validate(self, command):
        chunks = command.split(" ")
        err_message = 'error\nwrong command\n\n'
        len_chunks = len(chunks)
        # print(len_chunks)
        # "." in chunks[1] and
        if len_chunks < 2 or len_chunks > 4:
            return err_message

        if chunks[0] == "get":
            #  or ("." in chunks[1]))
            if len_chunks == 2:
                # print(chunks[1])
                return self._get(chunks[1])
            else:
                return err_message

        if chunks[0] == "put":
            if len_chunks == 4:
                try:
                    return self._put(chunks[1], float(chunks[2]), int(chunks[3]))
                except ValueError:
                    return err_message
                except IndexError:
                    return err_message

    def _get(self, key):
        reply = "ok\n"
        if key == "*":
            #print("I`m here! \n")
            for key, values in metrix_storage.items():
                for value in values:
                    reply = reply + key + " " + \
                        str(value[0]) + " " + str(value[1]) + '\n'

        elif key in metrix_storage:
            for value in metrix_storage[key]:
                reply = reply + key + " " + \
                    str(value[0]) + " " + str(value[1]) + '\n'
        else:
            pass
        #print(reply)
        return reply + "\n"

    def _put(self, key, value, timestamp):
        if not key in metrix_storage:
            metrix_storage[key] = list()

        if not (value, timestamp) in metrix_storage[key]:

            for metrix in metrix_storage[key]:
                
                if timestamp == metrix[1]:
                    index = metrix_storage[key].index(metrix)
                    #print(index)
                    metrix_storage[key].pop(index)
                    metrix_storage[key].insert(index, (value, timestamp))
                    return 'ok\n\n'

            metrix_storage[key].append((value, timestamp))
            metrix_storage[key].sort(key=lambda tup: tup[1])

        return 'ok\n\n'


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


#run_server('127.0.0.1', 8888)
