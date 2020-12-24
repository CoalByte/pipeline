class ProductionLine:
    def __init__(self, filter: list, name="undefined", on_section=None):
        def _internal(input):
            for f in filter:
                if f(input) is not True:
                    return False
            return True
        self.function = _internal
        self.data = []
        self.name = name
        self.on_section = on_section
        self.threads = []

    def section_data(self, data):
        self.data.append(data)

    def _get_thread(self, pid):
        for t in self.threads:
            if str(t.ident) == str(pid):
                return t
        return None

    def _execute_event(self, empty=None):
        if self.on_section is not None:
            self.on_section(self)
        self.threads.remove(self._get_thread(pid=threading.get_ident()))

    def exec_event(self, _thread=True):
        if _thread is True:
            t = threading.Thread(target=self._execute_event, args=[None], daemon=None, name=f"{self.name}_exec_thread")
            self.threads.append(t)
            t.start()
        else:
            self._execute_event()

class Pipeline:
    def __init__(self):
        self.lines = []

    def add_line(self, line: ProductionLine):
        self.lines.append(line)

    def process_data(self, data, single_sec=False):
        out = []
        for line in self.lines:
            if line.function(input=data) is True:
                line.section_data(data)
                line.exec_event()
                if single_sec is True:
                    return line
                else:
                    out.append(line)
        if single_sec is True:
            return None
        return out

    def _get_line(self, name):
        for l in self.lines:
            if l.name == name:
                return l
        return None

    def check(self, line_name, *, on_section=None):
        def wrapper(self, func):
            def _inner():
                self.add_check(func, line_name, on_section=on_section)
            return _inner()
        return wrapper
    
    def add_check(self, func, line_name, *, on_section=None):
        if self._get_line(line_name) is None:
            self.lines.append(ProductionLine(filter=[func], name=line_name, on_section=on_section))
