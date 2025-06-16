import copy

class CloneMixin:
    def deep_clone(self):
        return copy.deepcopy(self)

class NetElement(CloneMixin):
    def display(self, level=0, last=False, label=None):
        pass

class IP(NetElement):
    def __init__(self, ip_addr):
        self.ip_addr = ip_addr

    def display(self, level=0, last=False, label=None):
        prefix = "  " * level + ("\\-" if last else "+-")
        print(f"{prefix}{self.ip_addr}")

class HardwareUnit(NetElement):
    def __init__(self, description):
        self.description = description

class Processor(HardwareUnit):
    def __init__(self, cores, frequency):
        super().__init__("Processor")
        self.cores = cores
        self.frequency = frequency

    def display(self, level=0, last=False, label=None):
        prefix = "  " * level + ("\\-" if last else "+-")
        print(f"{prefix}{self.description}, {self.cores} cores @ {self.frequency}MHz")

class RAM(HardwareUnit):
    def __init__(self, capacity_mb):
        super().__init__("RAM")
        self.capacity_mb = capacity_mb

    def display(self, level=0, last=False, label=None):
        prefix = "  " * level + ("\\-" if last else "+-")
        print(f"{prefix}{self.description}, {self.capacity_mb} MiB")

class Storage(HardwareUnit):
    def __init__(self, capacity_gb, kind):
        name = "HDD" if kind.lower() == "hdd" else "SSD"
        super().__init__(name)
        self.capacity_gb = capacity_gb
        self.parts = []

    def add_part(self, size_gb, purpose):
        self.parts.append(StoragePartition(size_gb, purpose))

    def display(self, level=0, last=False, label=None):
        prefix = "  " * level + ("\\-" if last else "+-")
        print(f"{prefix}{self.description}, {self.capacity_gb} GiB")
        for i, part in enumerate(self.parts):
            last_part = i == len(self.parts) - 1
            part.display(level + 1, last_part, f"[{i}]")

class StoragePartition(NetElement):
    def __init__(self, size_gb, purpose):
        self.size_gb = size_gb
        self.purpose = purpose

    def display(self, level=0, last=False, label=None):
        prefix = "  " * level + ("\\-" if last else "+-")
        label_text = label if label else ""
        print(f"{prefix}{label_text}: {self.size_gb} GiB, {self.purpose}")

class Machine(NetElement):
    def __init__(self, hostname):
        self.hostname = hostname
        self.ips = []
        self.hardware_units = []

    def add_ip(self, ip_addr):
        self.ips.append(IP(ip_addr))

    def add_hardware(self, hw_unit):
        self.hardware_units.append(hw_unit)

    def display(self, level=0, last=False, label=None):
        prefix = "  " * level + ("\\-" if last else "+-")
        print(f"{prefix}Machine: {self.hostname}")

        # Выводим IP-адреса
        for i, ip in enumerate(self.ips):
            ip_last = (i == len(self.ips) - 1) and (len(self.hardware_units) == 0)
            ip.display(level + 1, ip_last)

        # Выводим оборудование
        for i, hw in enumerate(self.hardware_units):
            hw_last = (i == len(self.hardware_units) - 1)
            hw.display(level + 1, hw_last)

class Network(NetElement):
    def __init__(self, net_name):
        self.net_name = net_name
        self.machines = []

    def add_machine(self, machine):
        self.machines.append(machine)

    def find_machine(self, hostname):
        for m in self.machines:
            if m.hostname == hostname:
                return m
        return None

    def display(self, level=0, last=False, label=None):
        print(f"Network: {self.net_name}")
        for i, machine in enumerate(self.machines):
            machine_last = (i == len(self.machines) - 1)
            machine.display(level, machine_last)

if __name__ == "__main__":
    net = Network("MISIS network")

    m1 = Machine("server1.misis.ru")
    m1.add_ip("192.168.1.1")
    m1.add_hardware(Processor(4, 2500))
    m1.add_hardware(RAM(16000))
    net.add_machine(m1)

    m2 = Machine("server2.misis.ru")
    m2.add_ip("10.0.0.1")
    m2.add_hardware(Processor(8, 3200))
    storage = Storage(2000, "hdd")
    storage.add_part(500, "system")
    storage.add_part(1500, "data")
    m2.add_hardware(storage)
    net.add_machine(m2)

    net.display()

    found = net.find_machine("server1.misis.ru")
    print("\nLocated machine:", found.hostname if found else "None")

    clone_m1 = m1.deep_clone()
    clone_m1.hostname = "server1-copy.misis.ru"
    print("\nOriginal machine:")
    m1.display()
    print("\nCloned machine (changed):")
    clone_m1.display()
