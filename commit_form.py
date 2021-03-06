import npyscreen
import sqlite_utils
import git_utils
import curses

class CommitForm(npyscreen.ActionForm):
    def create(self,*args,**keywords):
        self.name = "Commit message"
        self.repo_name = ''
        self.repo_path = ''
        self.file_list = ''
        self.active_branch = 'master'
        self.commit_message = self.add_widget(npyscreen.TitleText,use_two_lines=False,name='Commit message:')
    def set_up_handlers(self):
        super(CommitForm,self).set_up_handlers()
        self.handlers.update({curses.KEY_ENTER:self.on_ok,"q": self.on_cancel})
    def beforeEditing(self):
        self.active_branch = git_utils.active_branch(self.repo_path)
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        if git_utils.tracked_branch(self.repo_path,self.active_branch) != None:
            temp_branch = self.active_branch+'-tmp'
            git_utils.create_branch(self.repo_path,temp_branch)
        git_utils.commit_files(self.repo_path,self.file_list,self.commit_message.value)
        self.parentApp.switchForm('MAIN')
