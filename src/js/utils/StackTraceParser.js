var fs = require('fs');
var argparse = require('argparse');
var StackTraceParser = require('stacktrace-parser');

var parser = new argparse.ArgumentParser();
parser.addArgument(['--exceptionfile']);
parser.addArgument(['--instrumentedfile']);
parser.addArgument(['--range']);

var args = parser.parseArgs();
var JALANGI_STOP = __dirname + '/../../../jalangi_tmp/jalangi_stop';

if (args.range) {
    var shouldStop = false;
    try {
        var exception = fs.readFileSync(args.exceptionfile, "utf8");
        var lines = StackTraceParser.parse(exception);
        var range = args.range.split(':');
        var begin = parseInt(range[0]);
        var end = parseInt(range[1]);

        for (var i = 0; i < lines.length; i++) {
            var line = lines[i];
            var file = line.file.replace(/^.*[\\\/]/, '');
            var lineNumber = parseInt(line.lineNumber);

            if (file === args.instrumentedfile && lineNumber >= begin && lineNumber <= end) {
                shouldStop = true;
                break;
            }
        }
    } finally {
        fs.writeFileSync(JALANGI_STOP, shouldStop, 'utf8');
    }
} else {
    fs.writeFileSync(JALANGI_STOP, 'false', 'utf8');
}
