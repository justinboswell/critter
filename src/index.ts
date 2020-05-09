
import fs from 'fs'
import process from 'process'

class LogEntry {
    constructor(
        public level: string,
        public time: string,
        public thread: string,
        public subject: string,
        public message: string,
        public id: string|undefined = undefined
    ) {
    }

    static PATTERN = new RegExp(/\[(?<level>[A-Z]+)\s*\] \[(?<time>.+?Z)\] \[(?<thread>[a-f0-9]+)\] \[(?<subject>[A-Za-z-_]+)\] - (?<message>.*(id=(?<id>0x[a-f0-9]+))?.+)/)
}

function parseLine(line: string) {
    let match = LogEntry.PATTERN.exec(line)
    if (match) {
        return new LogEntry(
            match[1],
            match[2],
            match[3],
            match[4],
            match[5],
            match[7]
        )
    }
    return null
}

const ignoredSubjects = new Set(['dns', 'event-loop', 'task-scheduler', 'Unknown'])
function isRelevantToHttp(entry: LogEntry) {
    return !ignoredSubjects.has(entry.subject)
}

function parseFile(path: string) {
    let entries = new Array<LogEntry>()
    let contents = fs.readFileSync(path, 'utf8')
    for (let line of contents.split('\n')) {
        let entry = parseLine(line)
        if (entry && isRelevantToHttp(entry)) {
            entries.push(entry)
        }
    }
    return entries
}

function *findConnectionManagers(entries: Array<LogEntry>) {
    for (let entry of entries) {
        if (entry.subject == 'connection-manager' && entry.message.startsWith('Successfully created')) {
            yield entry.id
        }
    }
}

const entries = parseFile(process.argv[2])
const mgrs = findConnectionManagers(entries)
