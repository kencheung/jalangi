from optparse import OptionParser
import sys
import commands
import os

class InstrumentCommand:
    name = "Instrument"
    description = "Instrument JavaScript source files"
    def execute(self,params):
       # if len(params) < 1:
       #     print "Instrument requires a filename"
       #     sys.exit(1)
        parser = OptionParser()
        (options, args) = parser.parse_args(args=params)
        (ff,out) = commands.instrument(os.path.abspath(args[0]) + ".js")
        print out

class AnalysisCommand:
    name = "Analysis"
    description = "Run a Jalangi Analysis"
    def execute(self, params):
        parser = OptionParser()
        parser.add_option("-a", "--analysis", dest="analysis",
                          help="Use analysis implemented in ANALYSIS", default="%NOT_SET")
        (options, args) = parser.parse_args(args=params)
        if len(args) < 1 or options.analysis == "%NOT_SET":
            print "Invalid command line"
            parser.print_help()
            sys.exit(1)
        print commands.analysis(options.analysis, os.path.abspath(args[0]))
        
COMMANDS = {"instrument" : InstrumentCommand,
            "analyze" : AnalysisCommand}

def print_help():
    print "The following Jalangi commands are avaliable:"
    for k,v in COMMANDS.iteritems():
        print "{} - {}".format(k, v.description)

def main():
    args = sys.argv
    if len(args) == 1:
        print_help()
        sys.exit(0)
    command_name = args[1]
    if not command_name in COMMANDS.keys():
        print "Unknown command {}".format(command_name)
        print_help()
        sys.exit(1)
    command = COMMANDS[command_name]()
    command.execute(args[2:])

if __name__ == "__main__":
    main()