import re
class Executor:
    def execute(self, cmd):
        cmd = cmd.strip('\n')
        self.stdin.write(cmd + '\n\n\n')
        finish = 'finished with exit status'
        echo_cmd = 'echo {}'.format(finish)
        shin = self.stdin
        self.stdin.flush()
        shout = []
        sherr = []
        for line in self.stdout:
            line = line.strip('\r\n')
            line = line.strip('\n')
            print("line data: " + str(len(line)))
            print(line)
            print("hostname data: " + self.hostname + str(len(self.hostname)))

            if str(line).endswith(cmd) or str(line).endswith(echo_cmd):
                # up for now filled with shell junk from stdin
                #print("starts with cmd or echo")
                shout = []
            elif (self.hostname + cmd) in str(line):
                print("command sent")

            elif str(line).startswith(str(self.hostname)):
                print("has HASH line")
                break
            else:
                # get rid of 'coloring and formatting' special characters
                print("appending to SHOUT")
                shout.append(re.compile(r'(\x9B|\x1B\[)[0-?]*[-/]*[@-~]').sub('', line).
                             replace('\b', '').replace('\r', ''))

        shout = shout[1:]
        return shin, shout, sherr
