import sublime
import os
from .javatar_actions import *


STATUS = "Javatar"
SETTINGSBASE = None
SETTINGS = None


def reset():
	getAction().addAction("javatar.util.util.reset", "Reset all settings")
	global SETTINGS, SETTINGSBASE
	SETTINGS = None
	SETTINGSBASE = None
	from .javatar_collections import resetSnippetsAndPackages
	resetSnippetsAndPackages()


def isReady():
	return SETTINGS is not None


def readSettings(config):
	getAction().addAction("javatar.util.util.read_settings", "Read settings")
	global SETTINGS, SETTINGSBASE
	SETTINGSBASE = config
	SETTINGS = sublime.load_settings(config)
	from .javatar_collections import loadSnippetsAndPackages
	loadSnippetsAndPackages()


def getSettings(key):
	project_data = sublime.active_window().project_data()
	if key in project_data:
		return project_data[key]
	return SETTINGS.get(key)


def setSettings(key, val, project=False):
	if project:
		project_data = sublime.active_window().project_data()
		project_data[key] = val
		sublime.active_window().set_project_data(project_data)
	else:
		SETTINGS.set(key, val)
		sublime.save_settings(SETTINGSBASE)


def isDebug():
	return getSettings("debug_mode")


def isStable():
	return str.lower(getSettings("package_channel")) != "dev"


def normalizePath(path):
	name = getPath("name", path)
	parent = getPath("parent", path)
	if parent != getPath("parent", parent):
		parent = normalizePath(parent)
	for dir_path in os.listdir(parent):
		if dir_path.lower() == name:
			return getPath("join", parent, dir_path)
	return path


def splitPath(path):
	rest, tail = os.path.split(path)
	if len(rest) <= 1:
		return tail,
	return splitPath(rest) + (tail,)


def joinPath(paths):
	outpath = ""
	for path in paths:
		outpath = os.path.join(outpath, path)
	return outpath


def mergePath(pathlist):
	outpath = ""
	for path in pathlist:
		outpath = getPath("join", outpath, path)
	return outpath


def showStatus(text, delay=None, require_java=True):
	if delay is None:
		delay = getSettings("status_delay")
	from .javatar_validator import isJava
	if not isJava() and require_java:
		return
	view = sublime.active_window().active_view()
	view.set_status(STATUS, text)
	if delay >= 0:
		sublime.set_timeout(hideStatus, delay)


def hideStatus():
	view = sublime.active_window().active_view()
	if view is not None:
		from .javatar_validator import isJava
		if isJava() and getSettings("show_package_path"):
			view.set_status(STATUS, "Package: " + toReadablePackage(getCurrentPackage(), True))
		else:
			view.erase_status(STATUS)


def toReadableSize(filepath):
	if filepath[0:8] == "Packages":
		filepath = sublime.packages_path()+filepath[8:]
	scales = [
		[1000**5, "PB"],
		[1000**4, "TB"],
		[1000**3, "GB"],
		[1000**2, "MB"],
		[1000**1, "KB"],
		[1000**0, "B"]
	]
	filesize = os.path.getsize(filepath)
	for scale in scales:
		if filesize >= scale[0]:
			break
	return str(int(filesize/scale[0]*100)/100)+scale[1]


def getCurrentPackage(relative=False):
	from .javatar_validator import isProject, isFile
	if not relative and isFile() and getPath("current_dir") is not None:
		return toPackage(getPath("current_dir"))
	elif not relative and isProject() and getPath("source_folder") is not None:
		return toPackage(getPath("source_folder"))
	else:
		return ""


def toReadablePackage(package, asPackage=False):
	if not asPackage:
		package = toPackage(package)
	if package == "":
		from .javatar_validator import isProject
		if isProject():
			package = "(Default Package)"
		else:
			package = "(Unknown Package)"
	return package


def toPackage(path, relative=True):
	if relative:
		path = getPath("relative", path, getPackageRootDir())
	package = ".".join(splitPath(path))
	from .javatar_java import normalizePackage
	return normalizePackage(package)


def getPackageRootDir(isSub=False):
	from .javatar_validator import isProject, isFile
	if isProject():
		return getPath("source_folder")
	elif isFile() and isSub:
		return getPath("current_dir")
	elif getPath("current_dir") is not None:
		return getPath("current_dir")
	else:
		return ""


def containsFile(directory, file_path):
	return os.path.normcase(os.path.normpath(file_path)).startswith(os.path.normcase(os.path.normpath(directory)))


def withoutExtension(file_path):
	for extension in getSettings("java_extensions"):
		if file_path.endswith("."+extension):
			return file_path[:-len(extension)-1]
	return file_path


def getClassName(file_path=None, view=None):
	from .javatar_validator import isFile
	if view is not None:
		classRegions = view.find_by_selector(getSettings("class_name_selector"))
		if len(classRegions) > 0:
			return view.substr(classRegions[0])
		else:
			return withoutExtension(getPath("name", view.file_name()))
	elif file_path is not None:
		return withoutExtension(getPath("name", file_path))
	else:
		if isFile():
			return getClassName(None, sublime.active_window().active_view())
	return None


def getPath(path_type="", dir_path="", dir_path2=""):
	window = sublime.active_window()
	if path_type == "source_folder":
		from .javatar_validator import isFile
		path = getSettings("source_folder")
		if path != "":
			return path
		if path is None:
			path = ""
		folders = window.folders()
		if len(folders) == 1:
			return folders[0]
		for folder in folders:
			if isFile() and containsFile(folder, getPath("current_file")):
				path = folder
				break
		return path
	elif path_type == "project_dir":
		folders = window.folders()
		if len(folders) == 1:
			return folders[0]
		elif len(folders) > 1:
			return getPath("parent", folders[0])
		for folder in folders:
			if isFile() and containsFile(folder, getPath("current_file")):
				return folder
				break
		return ""
	elif path_type == "current_dir":
		if getPath("current_file") is not None:
			return getPath("parent", getPath("current_file"))
		else:
			return None
	elif path_type == "current_file":
		return window.active_view().file_name()
	elif path_type == "parent":
		return os.path.dirname(dir_path)
	elif path_type == "relative":
		if dir_path != "" and dir_path2 != "":
			return os.path.relpath(dir_path, dir_path2)
		else:
			return ""
	elif path_type == "name":
		return os.path.basename(dir_path)
	elif path_type == "join":
		return os.path.join(dir_path, dir_path2)
	elif path_type == "exist":
		return os.path.exists(dir_path)
	elif path_type == "javatar_parent":
		name = __name__.split('.')
		return name[0]
	else:
		return ""
