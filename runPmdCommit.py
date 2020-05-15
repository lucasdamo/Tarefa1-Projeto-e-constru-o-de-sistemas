import git
import os
import csv

class AnalyzeCommit():
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.repo = git.repo.Repo(repo_dir)
    def setTargetCommit(self, hash):
        self.hash = hash
        self.target_commit = self.repo.commit(hash)
        self._setPreviousCommit()
        self._setCommitFiles()
    def _setPreviousCommit(self):
        list_commits = list(self.repo.iter_commits())
        self.previous_commit = list_commits[list_commits.index(self.target_commit) - 1]
    def _setCommitFiles(self):
        self.files = [key for key in self.target_commit.stats.files]

    def _resetToCommit(self, commit:git.Commit):
        self.repo.index.reset(commit, working_tree=True)

    def _runPmdForAllCommitFiles(self, sE = "start", format="csv"):
        str_files = ",".join([os.path.join(self.repo_dir, x) for x in self.files])
        cmd = f"{os.path.join(os.getcwd(), 'pmd-bin-6.22.0/bin/run.sh pmd')} -min 5 -l java -f csv -d {str_files} -R {os.path.join(os.getcwd(), 'rules.xml')} -b -no-cache > ./result/{sE}_{self.hash}.{format} 2>./benchmark/{sE}_{self.hash}.txt"
        print(cmd)
        os.system(cmd)
    def _separateCsvRow(self, text):
        with open(os.path.join(os.getcwd(), f'{self.hash}.csv'), 'a') as fd:
            writer = csv.writer(fd)
            writer.writerow([text])
    def _sanitizeCsv(self):
        header = '"Problem","Package","File","Priority","Line","Description","Rule set","Rule"'
        with open(f"{self.hash}.csv", "r") as f, open(f"{self.hash}_sanitized.csv", "a") as fw:
            lines = f.readlines()
            f.seek(0)
            fw.write(header + '\n')
            for line in lines:
                if line.strip("\n") != header:
                    fw.write(line)

    def analyzeCommit(self):
        self._resetToCommit(self.previous_commit)
        print(f"Analyzing commit {self.previous_commit.name_rev}")
        self._runPmdForAllCommitFiles(sE="start")
        print(f"Analyzing commit {self.target_commit.name_rev}")
        self._resetToCommit(self.target_commit)
        self._runPmdForAllCommitFiles(sE="end")


list_commits = []

ac = AnalyzeCommit("/home/lucas/Documents/PrestoDB/presto")

for commit in list_commits:
    ac.setTargetCommit("307d1cb83c7b8f264414c7a4e8f254296ddcc0e3")
    ac.analyzeCommit()
