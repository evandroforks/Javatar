import sublime
import sublime_plugin
import sys
from imp import reload
import hashlib
import urllib.request
import traceback
from ..parser.GrammarParser import GrammarParser
from ..core import (
    ActionHistory,
    JSONPanel,
    StatusManager
)
from ..utils import (
    Constant
)


class JavatarUtilsCommand(sublime_plugin.TextCommand):

    """
    Command for utility actions
    """

    def on_done(self, obj):
        """
        JSONPanel's on_done
        """
        print(str(sublime.encode_value(obj)))

    def on_cancel(self):
        """
        JSONPanel's on_cancel
        """
        print("Cancel")

    def run(self, edit, util_type="", text="", region=None, dest=None):
        """
        Run specified utility

        @param edit: edit object from Sublime Text buffer
        @param util_type: utility selector
        @param text: text to be used with edit object
        @param region: replace region (use with replace utility)
        @param dest: command description (use on dest method)
        """
        if util_type == "insert":
            self.view.insert(edit, 0, text)
        elif util_type == "add":
            self.view.insert(edit, self.view.size(), text)
        elif util_type == "replace":
            self.view.insert(edit, region, text)
        elif util_type == "clear":
            self.view.erase(edit, sublime.Region(0, self.view.size()))
        elif util_type == "set_read_only":
            self.view.set_read_only(True)
        elif util_type == "clear_read_only":
            self.view.set_read_only(False)
        elif util_type == "test" and Constant.is_debug():
            self.view.show_popup_menu(["A", "B"], self.nothing)
        elif util_type == "remote_hash":
            sublime.active_window().show_input_panel("URL:", "", self.remote_hash, None, None)
        elif util_type == "hash":
            print(hashlib.sha256(self.view.substr(sublime.Region(0, self.view.size())).encode("utf-8")).hexdigest())
        elif util_type == "tojson":
            jsonObj = sublime.decode_value(self.view.substr(sublime.Region(0, self.view.size())))
            self.view.replace(edit, sublime.Region(0, self.view.size()), sublime.encode_value(jsonObj, True))
        elif util_type == "json_test" and Constant.is_debug():
            panel = JSONPanel(window=self.view.window(), on_done=self.on_done, on_cancel=self.on_cancel)
            view = panel.open("JSONTest.json")
            sublime.set_timeout(lambda: view.run_command("javatar_utils", {"util_type": "insert", "text": "{\n}"}), 50)
        elif util_type == "parse":
            sublime.active_window().show_input_panel("Parse Parameter:", "", self.parse_code, None, None)
        elif util_type == "reload" and Constant.is_debug():
            ActionHistory.add_action("javatar.commands.utils.utils.reload", "Reload Javatar")
            print("Reloading Javatar...")
            for mod in tuple(sys.modules.keys()):
                if mod.lower().startswith("javatar"):
                    print("Reloading module " + mod + "...")
                    reload(sys.modules[mod])
            from ..Javatar import plugin_loaded
            plugin_loaded()

    def parse_code(self, selector):
        """
        Parse code against Java grammar

        @param selector: scope selector (refer to GrammarParser's selector)
        """
        try:
            scope = GrammarParser(sublime.decode_value(sublime.load_resource("Packages/Javatar/grammars/Java8.javatar-grammar")))
            parse_output = scope.parse_grammar(self.view.substr(sublime.Region(0, self.view.size())))
            status_text = ""
            if parse_output["success"]:
                if selector == "":
                    nodes = scope.find_all()
                elif selector == "#":
                    selections = self.view.sel()
                    nodes = scope.find_by_region([0, 0])
                    if selections:
                        first_sel = selections[0]
                        if first_sel.empty():
                            nodes = scope.find_by_region([first_sel.begin(), first_sel.end()])
                        else:
                            nodes = scope.find_inside_region([first_sel.begin(), first_sel.end()])
                else:
                    nodes = scope.find_by_selectors(selector)
                if selector != "#":
                    status_text = "Parsing got {} tokens".format(len(nodes))
                for node in nodes:
                    if selector == "#":
                        if status_text == "":
                            status_text += node["name"]
                        else:
                            status_text += " " + node["name"]
                    else:
                        print("#{begin}:{end} => {name}".format_map(node))
                        print("   => {value}".format_map(node))

                print("Total: {} tokens".format(len(nodes)))
            if selector != "#":
                if status_text != "" and str(parse_output["end"]) == str(self.view.size()):
                    status_text += " in {elapse_time:.2f}s".format(elapse_time=scope.get_elapse_time())
                else:
                    status_text = "Parsing failed [" + str(parse_output["end"]) + "/" + str(self.view.size()) + "] in {elapse_time:.2f}s".format(elapse_time=scope.get_elapse_time())
            print("Ending: " + str(parse_output["end"]) + "/" + str(self.view.size()))
            print("Parsing Time: {elapse_time:.2f}s".format(elapse_time=scope.get_elapse_time()))
            StatusManager.show_status(status_text)
        except Exception:
            print("Error occurred while parsing")
            traceback.print_exc()

    def remote_hash(self, url):
        """
        Print hash of data from URL

        @param url: URL to fetch data
        """
        try:
            urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler()))
            data = urllib.request.urlopen(url).read()
            datahash = hashlib.sha256(data).hexdigest()
            print("Hash: " + datahash)
        except Exception:
            print("Error occurred while remote_hash")
            traceback.print_exc()

    def nothing(self, index=-1):
        """
        Dummy method for testing test utility
        """
        pass

    def description(self, util_type="", text="", region=None, dest=None):
        """
        Returns command description (which will display on undo/redo menu)

        @params are same as run method except no edit argument
        """
        return dest


class JavatarReloadPackagesCommand(sublime_plugin.WindowCommand):

    """
    Command to reload installed packages (used on install/uninstall packages)
    """

    def run(self):
        ActionHistory.add_action(
            "javatar.commands.utils.reload_packages", "Reload Packages"
        )
        # reset_packages()
        # load_packages()
