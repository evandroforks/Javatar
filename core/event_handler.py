import sublime_plugin


class _EventHandler:

    """
    A multiple event listener wrapper to simplify the event handlings
    """

    ON_NEW = 0x1
    ON_NEW_ASYNC = 0x2
    ON_CLONE = 0x4
    ON_CLONE_ASYNC = 0x8
    ON_LOAD = 0x10
    ON_LOAD_ASYNC = 0x20
    ON_PRE_CLOSE = 0x40
    ON_CLOSE = 0x80
    ON_PRE_SAVE = 0x100
    ON_PRE_SAVE_ASYNC = 0x200
    ON_POST_SAVE = 0x400
    ON_POST_SAVE_ASYNC = 0x800
    ON_MODIFIED = 0x1000
    ON_MODIFIED_ASYNC = 0x2000
    ON_SELECTION_MODIFIED = 0x4000
    ON_SELECTION_MODIFIED_ASYNC = 0x8000
    ON_ACTIVATED = 0x10000
    ON_ACTIVATED_ASYNC = 0x20000
    ON_DEACTIVATED = 0x40000
    ON_DEACTIVATED_ASYNC = 0x80000
    ON_POST_TEXT_COMMAND = 0x100000
    ON_POST_WINDOW_COMMAND = 0x800000

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.handlers = []

    def register_handler(self, handler, events=0):
        """
        Add event listener to event handler
        """
        self.handlers.append([handler, events])

    def unregister_handler(self, handler):
        """
        Remove event listener from event handler
        """
        for hdr in self.handlers:
            if hdr[0] == handler:
                self.handlers.remove(hdr)
                break

    def on_new(self, view):
        for handler, event in self.handlers:
            if event & self.ON_NEW > 0:
                if hasattr(handler, "on_new"):
                    handler.on_new(view)
                else:
                    handler(view)

    def on_new_async(self, view):
        for handler, event in self.handlers:
            if event & self.ON_NEW_ASYNC > 0:
                if hasattr(handler, "on_new_async"):
                    handler.on_new_async(view)
                else:
                    handler(view)

    def on_clone(self, view):
        for handler, event in self.handlers:
            if event & self.ON_CLONE > 0:
                if hasattr(handler, "on_clone"):
                    handler.on_clone(view)
                else:
                    handler(view)

    def on_clone_async(self, view):
        for handler, event in self.handlers:
            if event & self.ON_CLONE_ASYNC > 0:
                if hasattr(handler, "on_clone_async"):
                    handler.on_clone_async(view)
                else:
                    handler(view)

    def on_load(self, view):
        for handler, event in self.handlers:
            if event & self.ON_LOAD > 0:
                if hasattr(handler, "on_load"):
                    handler.on_load(view)
                else:
                    handler(view)

    def on_load_async(self, view):
        for handler, event in self.handlers:
            if event & self.ON_LOAD_ASYNC > 0:
                if hasattr(handler, "on_load_async"):
                    handler.on_load_async(view)
                else:
                    handler(view)

    def on_pre_close(self, view):
        for handler, event in self.handlers:
            if event & self.ON_PRE_CLOSE > 0:
                if hasattr(handler, "on_pre_close"):
                    handler.on_pre_close(view)
                else:
                    handler(view)

    def on_close(self, view):
        for handler, event in self.handlers:
            if event & self.ON_CLOSE > 0:
                if hasattr(handler, "on_close"):
                    handler.on_close(view)
                else:
                    handler(view)

    def on_pre_save(self, view):
        for handler, event in self.handlers:
            if event & self.ON_PRE_SAVE > 0:
                if hasattr(handler, "on_pre_save"):
                    handler.on_pre_save(view)
                else:
                    handler(view)

    def on_pre_save_async(self, view):
        for handler, event in self.handlers:
            if event & self.ON_PRE_SAVE_ASYNC > 0:
                if hasattr(handler, "on_pre_save_async"):
                    handler.on_pre_save_async(view)
                else:
                    handler(view)

    def on_post_save(self, view):
        for handler, event in self.handlers:
            if event & self.ON_POST_SAVE > 0:
                if hasattr(handler, "on_post_save"):
                    handler.on_post_save(view)
                else:
                    handler(view)

    def on_post_save_async(self, view):
        for handler, event in self.handlers:
            if event & self.ON_POST_SAVE_ASYNC > 0:
                if hasattr(handler, "on_post_save_async"):
                    handler.on_post_save_async(view)
                else:
                    handler(view)

    def on_modified(self, view):
        for handler, event in self.handlers:
            if event & self.ON_MODIFIED > 0:
                if hasattr(handler, "on_modified"):
                    handler.on_modified(view)
                else:
                    handler(view)

    def on_modified_async(self, view):
        for handler, event in self.handlers:
            if event & self.ON_MODIFIED_ASYNC > 0:
                if hasattr(handler, "on_modified_async"):
                    handler.on_modified_async(view)
                else:
                    handler(view)

    def on_selection_modified(self, view):
        for handler, event in self.handlers:
            if event & self.ON_SELECTION_MODIFIED > 0:
                if hasattr(handler, "on_selection_modified"):
                    handler.on_selection_modified(view)
                else:
                    handler(view)

    def on_selection_modified_async(self, view):
        for handler, event in self.handlers:
            if event & self.ON_SELECTION_MODIFIED_ASYNC > 0:
                if hasattr(handler, "on_selection_modified_async"):
                    handler.on_selection_modified_async(view)
                else:
                    handler(view)

    def on_activated(self, view):
        for handler, event in self.handlers:
            if event & self.ON_ACTIVATED > 0:
                if hasattr(handler, "on_activated"):
                    handler.on_activated(view)
                else:
                    handler(view)

    def on_activated_async(self, view):
        for handler, event in self.handlers:
            if event & self.ON_ACTIVATED_ASYNC > 0:
                if hasattr(handler, "on_activated_async"):
                    handler.on_activated_async(view)
                else:
                    handler(view)

    def on_deactivated(self, view):
        for handler, event in self.handlers:
            if event & self.ON_DEACTIVATED > 0:
                if hasattr(handler, "on_deactivated"):
                    handler.on_deactivated(view)
                else:
                    handler(view)

    def on_deactivated_async(self, view):
        for handler, event in self.handlers:
            if event & self.ON_DEACTIVATED_ASYNC > 0:
                if hasattr(handler, "on_deactivated_async"):
                    handler.on_deactivated_async(view)
                else:
                    handler(view)

    def post_text_command(self, view, command_name, args):
        for handler, event in self.handlers:
            if event & self.ON_POST_TEXT_COMMAND > 0:
                if hasattr(handler, "on_post_text_command"):
                    handler.on_post_text_command(view, command_name, args)
                else:
                    handler(view, command_name, args)

    def post_window_command(self, window, command_name, args):
        for handler, event in self.handlers:
            if event & self.ON_POST_WINDOW_COMMAND > 0:
                if hasattr(handler, "on_post_window_command"):
                    handler.on_post_window_command(window, command_name, args)
                else:
                    handler(window, command_name, args)


def EventHandler():
    return _EventHandler.instance()


class EventListener(sublime_plugin.EventListener):
    def on_new(self, view):
        EventHandler().on_new(view)

    def on_new_async(self, view):
        EventHandler().on_new_async(view)

    def on_clone(self, view):
        EventHandler().on_clone(view)

    def on_clone_async(self, view):
        EventHandler().on_clone_async(view)

    def on_load(self, view):
        EventHandler().on_load(view)

    def on_load_async(self, view):
        EventHandler().on_load_async(view)

    def on_pre_close(self, view):
        EventHandler().on_pre_close(view)

    def on_close(self, view):
        EventHandler().on_close(view)

    def on_pre_save(self, view):
        EventHandler().on_pre_save(view)

    def on_pre_save_async(self, view):
        EventHandler().on_pre_save_async(view)

    def on_post_save(self, view):
        EventHandler().on_post_save(view)

    def on_post_save_async(self, view):
        EventHandler().on_post_save_async(view)

    def on_modified(self, view):
        EventHandler().on_modified(view)

    def on_modified_async(self, view):
        EventHandler().on_modified_async(view)

    def on_selection_modified(self, view):
        EventHandler().on_selection_modified(view)

    def on_selection_modified_async(self, view):
        EventHandler().on_selection_modified_async(view)

    def on_activated(self, view):
        EventHandler().on_activated(view)

    def on_activated_async(self, view):
        EventHandler().on_activated_async(view)

    def on_deactivated(self, view):
        EventHandler().on_deactivated(view)

    def on_deactivated_async(self, view):
        EventHandler().on_deactivated_async(view)

    def post_text_command(self, view, command_name, args):
        EventHandler().post_text_command(view, command_name, args)

    def post_window_command(self, window, command_name, args):
        EventHandler().post_window_command(window, command_name, args)
