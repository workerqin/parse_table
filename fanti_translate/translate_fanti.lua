#!/usr/local/bin/lua
require("lposix")

--[[
--msg_id : "防御":1
--id_msg : 1:防御
--]]
local AllMsg = {["msg_id"] = {}, ["id_msg"] = {}, ["MaxId"] = 0}

local POSTFIX = {"c", "h"}

local function Log(...)
	print(...)
end

local function repr(t)
	for k,v in pairs(t) do
		print(k,v)
	end
end

local function GetNewMsgId()
	AllMsg["MaxId"] = AllMsg["MaxId"] + 1
	return AllMsg["MaxId"]
end

local function AddMsgId(id, msg)
	if AllMsg["msg_id"][msg] == nil then
		AllMsg["msg_id"][msg] = id
	end

	if AllMsg["id_msg"][id] == nil then
		AllMsg["id_msg"][id] = msg
	end

	if id > AllMsg["MaxId"] then
		AllMsg["MaxId"] = id
	end
end

local function GetMsg(id)
	return AllMsg["id_msg"][id]
end

local function GetMsgId(msg)
	if AllMsg["msg_id"][msg] == nil then
		return GetNewMsgId(), true
	else
		return AllMsg["msg_id"][msg], false
	end
end

local function DirPath(path, filename)
	local pathlen = string.len(path)
	if string.sub(path, pathlen, pathlen) == "/" then
		return path .. filename
	else
		return path .. "/" .. filename
	end
end

function HasCn(s)
	if not s or #s < 2 then
		return false
	end
	for i=1, #s do
		if string.byte(s, i, i) >= 0xa1 then
			return true
		end
	end
	return false
end

local function IsUTF8(filename)
	local tmp = io.popen("enca " .. filename)
	local utf = tmp:read("*a")
	tmp:close()

	if string.find(utf, "UTF") then
		return true
	else
		return false
	end
end

local function ToUTF8(ToPathFile)
	if IsUTF8(ToPathFile) then
		return false
	end

	local cmd = "iconv -f gb18030 -t utf-8 %s > /tmp/jianti_fanti_utf_8.tmp"
	local tmp = io.popen(string.format(cmd, ToPathFile))
	local utf = tmp:read("*a")
	tmp:close()

	if string.find(utf, "cannot") then
		return false
	end

	local mvcmd = "cp /tmp/jianti_fanti_utf_8.tmp %s"
	os.execute(string.format(mvcmd, ToPathFile))

	return true
end

local novalidpath = {"etc/map/", "etc/patch/", ".svn", ".xls"}

local function IsValidFile(filename)
	if filename == nil then
		return false
	end

	local len = string.len(filename)

	if string.sub(filename, len, len) == "~" then
		return false
	end

	for _, path in pairs(novalidpath) do
		if string.find(filename, path) then
			return false
		end
	end

	return true
end

local function RebuildMsgId(MsgFile)
	local FanTiFile = io.open(MsgFile)
	if FanTiFile == nil then
		return
	end

	for line in FanTiFile:lines() do
		local CnId, Data = string.match(line, "(FS_MSG_ID_%d+)=(.*)")
		if CnId then
			CnId = string.gsub(CnId, "FS_MSG_ID_", "")
			AddMsgId(tonumber(CnId), Data)
		end
	end
	
	Log("build msg file, max msg id :" .. AllMsg["MaxId"])

	FanTiFile:close()
end

-- 全局共用
local function ExtractFile(From, To)
	if not IsValidFile(From) then
		return
	end

	local fh2 = io.open(To, "a+")

	print("extract file: ".. From)

	local function repl(str)
		local Key = nil
		if HasCn(str) then
			local index, new = GetMsgId(str)
			Key = "FS_MSG_ID_" .. index

			if new then
				AddMsgId(index, str)
				fh2:write(Key .. "=" .. str .."\n")
			end

			return Key 
		end
	end

	local src = {} 
	local fh1 = io.open(From)
	for line in fh1:lines() do
		line = string.gsub(line, '(%"[^\\\n]-%")', repl)
		table.insert(src, line)
	end

	local s = table.concat(src, "\n") .. "\n"

	fh1:close()
	fh1 = io.open(From, "w+")
	fh1:write(s)
	fh1:close()
	fh2:close()
end

local function ExtractPath(Path, ToFile)
	local stat = posix.stat(Path)
	if stat == nil then
		return
	end

	if stat.type ~= "directory" then
		ExtractFile(Path, ToFile)
		return
	end

	for _,file in ipairs(posix.dir(Path)) do
		if string.sub(file, 1, 1) ~= "." then
			local PathFile = DirPath(Path, file)
			local stat = posix.stat(PathFile)
			if stat then
				if stat.type == "directory" then
					ExtractPath(PathFile, ToFile)
				else
					for _, postfix in ipairs(POSTFIX) do
						if string.find(PathFile, "%."..postfix.."$") then
							ExtractFile(PathFile, ToFile)
						end
					end
				end
			else
				Log("nil path:".. PathFile)
			end
		end
	end
end

local function RestoreFile(ToPathFile)
	if not IsValidFile(ToPathFile) then
		return
	end

	local fh1 = io.open(ToPathFile, "r+")
	local FileData = fh1:read("*a")
	fh1:close()

	local function repl(CnId)
		CnId = string.gsub(CnId, "FS_MSG_ID_", "")
		local Data = GetMsg(tonumber(CnId))
		return tostring(Data)
	end

	FileData = string.gsub(FileData, "(FS_MSG_ID_%d+)", repl)
	--解决引号嵌套的问题,调用gsub两次 
	FileData = string.gsub(FileData, "(FS_MSG_ID_%d+)", repl)

	fh1 = io.open(ToPathFile, "w+")
	fh1:write(FileData)
	fh1:close()

	print("restore path: ".. ToPathFile)
end

local function RestorePath(ToPath)
	local stat = posix.stat(ToPath)
	if stat == nil then
		return
	end

	if stat.type ~= "directory" then
		RestoreFile(ToPath)
		return
	end

	for _, file in ipairs(posix.dir(ToPath)) do
		if string.sub(file, 1, 1) ~= "." then
			local ToPathFile = DirPath(ToPath, file)
			if posix.stat(ToPathFile).type == "directory" then
				RestorePath(ToPathFile)
			else
				RestoreFile(ToPathFile)
			end
		end
	end
end

--[[
local ExChar = {["～"] = "\\~", ["／"] = "\\/"}
local function ExchangeChar(filename)
	local tmp = filename .. ".tmp"

	os.execute(string.format([=[sed "s/～/\~/g" %s > %s]=], filename, tmp))
	os.execute(string.format("mv %s %s", tmp, filename))
end
--]]
local function ToFanTi(filename, toFile)
	--ExchangeChar(filename)
	
	local cmd = string.format("autob5 < %s > /tmp/to_fan_ti_tmp.txt", filename)
	os.execute(cmd)

	cmd = string.format("iconv -f big5 -t utf-8 /tmp/to_fan_ti_tmp.txt > %s", toFile)

	local tmp = io.popen(cmd)
	local msg = tmp:read("*a")
	if string.find(msg, "cannot") then
		print("error: " .. msg)
		return
	end

	print("exchange to traditional chinese: ".. toFile)
end

local function ExchangeFile(filename)
	if not IsValidFile(filename) then
		return
	end

	if ToUTF8(filename) then
		print("exchange to utf-8: ".. filename)
	end
end

local function ExchangePath(path)
	local stat = posix.stat(path)
	if stat == nil then
		return
	end

	if stat.type ~= "directory" then
		ExchangeFile(path)
		return
	end

	for _, file in ipairs(posix.dir(path)) do
		if string.sub(file, 1, 1) ~= "." then
			local pathfile = DirPath(path, file)
			if posix.stat(pathfile).type == "directory" then
				ExchangePath(pathfile)
			else
				ExchangeFile(pathfile)
			end
		end
	end
end

local Cmds = {"iconv", "enca", "autob5"}
local CmdPath = {"/usr/bin/", "/usr/local/bin/"}

local function CheckCmd()
	local result = true
	for _, cmd in ipairs(Cmds) do
		local find = false
		for _, path in ipairs(CmdPath) do
			local tmp = io.popen(string.format("find %s -name %s", path, cmd))
			local msg = tmp:read("*a")
			tmp:close()

			if string.find(msg, cmd) then
				find = true
			end
		end
		if not find then
			print("cannot find cmd: " .. cmd)
			result = false
		end
	end

	return result
end

local function ShowHelp()
	print("translate fanti tool")
	print("==========================================")
	print("usage as:")
	print("	extract <frompath> <topath>")
	print("	restore <frompath> <topath>")
	print("	tofanti <fromfile> <tofile>")
	print("	file2utf <filepath>")
	print("==========================================")
	print("	*default process: extract -> toFanti -> File2UTF -> restore")
end

if #arg < 1 then
	print("")
	CheckCmd()
	print("")
	ShowHelp()
	return
end

if not CheckCmd() then
	print("please install cmd, you can install from port")
	return
end

local Action = arg[1]

if Action == "extract" then
	local frompath = arg[2]
	local topath = arg[3]

	if posix.stat(frompath) == nil then
		print("<frompath> error, path: " .. frompath)
		return
	end

	RebuildMsgId(topath)
	print("msg file have msg: " .. AllMsg["MaxId"])
	ExtractPath(frompath, topath)

elseif Action == "restore" then
	local frompath = arg[2]
	local topath = arg[3]

	if posix.stat(frompath) == nil then
		print("<frompath> error, path: " .. frompath)
		return
	end

	RebuildMsgId(frompath)
	print("msg file have msg: " .. AllMsg["MaxId"])
	RestorePath(topath)

elseif Action == "tofanti" then
	local path = arg[2]
	if posix.stat(path) == nil then
		print("<frompath> error, path: " .. path)
		return
	end
	ToFanTi(path, arg[3])
elseif Action == "file2utf" then
	local path = arg[2]
	if posix.stat(path) == nil then
		print("<frompath> error, path: " .. path)
		return
	end
	ExchangePath(path)
else 
	print("arg error!")
	ShowHelp()
end
