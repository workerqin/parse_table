function is_home_map_key(key)
	if key == "zones" or key == "buildings" or key == "gm" then
		return 1
	end
	return 0
end

function serial_map(data, pre)
	pre = pre .. "   "
	local message = "([\n"
	for k, v in pairs(data) do
		local v_str = ""
		local k_str = ""
		if is_home_map_key(k) == 1 then
			v_str = serial_map(v, pre)
		else
			v_str = serial_lpc(v, pre)
		end
		k_str = serial_lpc(k, pre)
		local tmp = string.format("%s%s: %s,\n", pre, k_str, v_str)
		message = message .. tmp
	end
	return message .. pre .. "])"
end

function serial_array(data, pre)
	pre = pre .. "   "
	local message = "\n" .. pre .. "({"
	-- for k, v in pairs(data) do
	for k = 1, #data do
		v = data[k]
		-- local k_str = serial_lpc(k, pre)
		local v_str = serial_lpc(v, pre)
		local tmp = string.format("%s, ", v_str)
		message = message .. tmp
	end
	return message .. "})"
end

function serial_number(data)
	return string.format("%d", data)
end

function serial_string(data)
	return string.format("\"%s\"", data)
end

function serial_bool(data)
	if data then
		return "1"
	else
		return "0"
	end
end

function is_array(data)
	for k, v in pairs(data) do
		t = type(k)
		len = #data
		if t ~= "number" then
			return 0
		elseif k > len then
			return 0
		end
	end
	return 1
end


function serial_lpc(data, pre)
	t = type(data)
	if t == "table" then
		if is_array(data) == 1 then
			return serial_array(data, pre)
		else
			return serial_map(data, pre)
		end
	elseif t == "string" then
		return serial_string(data)
	elseif t == "number" then
		return serial_number(data)
	elseif t == "boolean" then
		return serial_bool(data)
	else
		return ""
		-- error("canot serial" .. t)
	end
end

format_str = " \
static mapping data = %s; \
\
\
\
mapping get_data() { \
	return data; \
} \
"

function parse_file(file_path, output_file)
	data = dofile(file_path)
	message = serial_lpc(data, "")
	message = string.format(format_str, message)
	f = assert(io.open(output_file, "w"))
	f:write(message);
	f:close()
end

function get_dir_files(dir_path)
	local files = {}     -- new array
	local i = 1
	os.execute("ls -l " .. dir_path .. " > temp.txt")
	io.input("temp.txt")
	for line in io.lines() do
		_, _, filename = string.find(line, "(%a[%x_]+)%.lua")
		if filename ~= nil then
			files[i] = filename
			i = i + 1
		end
	end
	return files
end

function parse_dir(dir_path, output_file)
	files = get_dir_files(dir_path)
	message = ""
	data = {}
	for _, file in pairs(files) do
		_data = dofile(dir_path .. file .. ".lua")
		data[file] = _data
	end
	info = serial_lpc(data, "")
	message = message .. info
	message = string.format(format_str, message)
	f = assert(io.open(output_file, "w"))
	f:write(message);
	f:close()
end

function is_dir(path) 
	start,_ = string.find(path, "/$")
	return start
end

if is_dir(arg[1]) == nil then
	parse_file(arg[1], arg[2])
else
	parse_dir(arg[1], arg[2])
end
