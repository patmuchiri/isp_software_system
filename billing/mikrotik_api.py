import routeros_api

class MikroTikAPI:
    """Class to interact with MikroTik Router via API"""
    
    def __init__(self, host="102.215.32.180", username="pat", password="#@phenom2024", port=8728):
        """Initialize MikroTik credentials and connection."""
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        """Establish connection to the MikroTik router."""
        try:
            connection = routeros_api.RouterOsApiPool(
                self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                plaintext_login=True
            )
            self.connection = connection.get_api()
            print("Connected to MikroTik Router")
        except Exception as e:
            print(f"Failed to connect to MikroTik Router: {e}")
            self.connection = None

    def disconnect(self):
        """Close the connection to the MikroTik router."""
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Disconnected from MikroTik Router")

    def add_queue(self, static_ip, upload_speed, download_speed):
        """
        Add a queue for a client with the given static IP and bandwidth limits.
        """
        if not self.connection:
            self.connect()
        if self.connection:
            try:
                bandwidth = int(upload_speed)
                bandwidthformat = f"{bandwidth}M/{bandwidth}"
                # Add the queue on the MikroTik router
                api = self.connection
                api.get_resource('/queue/simple').add(
                    name=f"client_{static_ip}",
                    target=static_ip,
                    max_limit = bandwidthformat
                )
                print(f"Queue added for {static_ip} with {upload_speed} Mbps upload and {download_speed} Mbps download.")
            except Exception as e:
                print(f"Failed to add queue: {e}")
            finally:
                self.disconnect()

    def remove_queue(self, static_ip):
        """
        Remove the queue for a client with the given static IP.
        """
        if not self.connection:
            self.connect()
        if self.connection:
            try:
                api = self.connection
                queues = api.get_resource('/queue/simple')

                # Find and remove the queue associated with the static IP
                queue_list = queues.get(target=static_ip)
                for queue in queue_list:
                    queues.remove(id=queue['id'])
                print(f"Queue removed for {static_ip}")
            except Exception as e:
                print(f"Failed to remove queue: {e}")
            finally:
                self.disconnect()

    def get_all_queues(self):
        """
        Retrieve all queues from the MikroTik router.
        """
        if not self.connection:
            self.connect()
        if self.connection:
            try:
                api = self.connection
                queues = api.get_resource('/queue/simple')
                all_queues = queues.get()
                print(f"Retrieved {len(all_queues)} queues from MikroTik")
                return all_queues
            except Exception as e:
                print(f"Failed to retrieve queues: {e}")
            finally:
                self.disconnect()
        return []
