
import sublime
import sublime_plugin
import subprocess
import os

PACKAGE_NAME = 'Envoy'
SETTINGS_FILE = PACKAGE_NAME + '.sublime-settings'
settings = None

class EnvoyCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        global commands
        global settings
        global file_name

        commands = []
        file_name = self.view.file_name()

        settings = sublime.load_settings(SETTINGS_FILE)
        commandsJSon = settings.get("commands")


        for command in commandsJSon:
            commands.append(command['command'])

        window = sublime.active_window()
        window.show_quick_panel(commands, self.choice, sublime.MONOSPACE_FONT)

    def choice(self, choice):
        if choice >= 0:
            envoy_path = settings.get("envoy_path")
            command = commands[choice]

            commandArray = command.split('::')
            project = commandArray[0]
            task = commandArray[1]

            try:
                index = file_name.index(project)
            except ValueError:
                index = -1
            if index >= 0:

                projectLen = len(project)
                folder = file_name[:index+projectLen]

                commandTask = 'php ' + envoy_path + ' run ' + task
                os.chdir(folder)
                subprocess.Popen(commandTask, cwd=folder, shell=True)
                print(commandTask + ' on folder: ' + folder)
