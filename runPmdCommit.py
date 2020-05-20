import git
import os
import csv

class AnalyzeCommit():
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.repo = git.repo.Repo(repo_dir)
        self.list_commits = list(self.repo.iter_commits())
    def setTargetCommit(self, hash):
        self.hash = hash
        self.target_commit = self.repo.commit(hash)
        self._setPreviousCommit()
        self._setCommitFiles()
    def _setPreviousCommit(self):
        self.previous_commit = self.list_commits[self.list_commits.index(self.target_commit) + 1]
    def _setCommitFiles(self):
        self.files = [key for key in self.target_commit.stats.files]
    def _resetToCommit(self, commit:git.Commit):
        #self.repo.index.reset(commit, working_tree=True)
        self.repo.head.reset(commit, working_tree=True, index=True)
    def _selectExistentFiles(self):
        return_list = []
        for file in self.files:
            if os.path.isfile(os.path.join(self.repo_dir, file)):
                return_list.append(file)
        return return_list

    def _runPmdForAllCommitFiles(self, sE = "start", format="csv"):
        files = self._selectExistentFiles()
        str_files = ",".join([os.path.join(self.repo_dir, x) for x in files])
        cmd = f"{os.path.join(os.getcwd(), 'pmd-bin-6.22.0/bin/run.sh pmd')} -min 5 -l java -f csv -d {str_files} -R {os.path.join(os.getcwd(), 'rules.xml')} -b -no-cache > ./result/{self.hash}_{sE}.{format} 2>./benchmark/{self.hash}_{sE}.txt"
        print(cmd)
        os.system(cmd)

    def analyzeCommit(self):
        self._resetToCommit(self.previous_commit)
        print(f"Analyzing commit {self.previous_commit.name_rev}")
        self._runPmdForAllCommitFiles(sE="start")
        print(f"Analyzing commit {self.target_commit.name_rev}")
        self._resetToCommit(self.target_commit)
        self._runPmdForAllCommitFiles(sE="end")


list_commits = ["0052bd769dcbdd6c9c24a8160b2f9b65f60aa444","029aa841fbf083ff64e2d9e4fdce541b5766683d","080a6a124ad5c96712797ab106494e50b3b40cad","0ebc22050b6e93e2f1dd0d3e5fdc2dbe3c01333a","17283ddd89f5586466d75c7b5cd9c85c0d0bda03","24771e5b9b1765f498d717a8a600ca7d2ee80bfc","27c35db739b0146b2a5e96314d1165517a10a256","2ac73e10477b08a9f0a3b0d4f0e842ede86a1fda","34cea981c7fadfca67a752c0f09f78264aa03217","35a8e4309d7fecfc61e1a651a53c2acffe38c747","4c090723e893b9b25236b5dfa117dc2b4a63aae3","9b12138820908daa88f33077b4727cee98caf86b","a79933e31de2b7115aa7140e027ca47007fbf2d2","abbac155b0ad4f25af4b1fafcaa9fd2df06b31ac","d883ecb403129c8477b8929c02b83d5fde65f7a3","e442f69509043d1135445f29a4a5d86f9bb64017","e81b812b91b019e589ca1520eef22cdaf3735fbc","ff389508b9736fb0d8b114aa3a629b11f151534e","ffb68b88cd9a5346480798ce50167da8bf3cd1bc","ffe309dd7611f3f72b78e1dca5bb93bb6bad9a5e"]
ac = AnalyzeCommit("/home/lucas/Documents/PrestoDB/presto")

for commit in list_commits:
    ac.setTargetCommit(commit)
    ac.analyzeCommit()

