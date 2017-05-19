

--add current work dir to package path
local info = debug.getinfo(1, 'S')
--local p = string.gsub(info.source, "[^\\/]*\\.lua", "")
local p = string.gsub(info.source, "([^/]*).lua", "")
p = string.gsub(p, "@", "")

local m_package_path = package.path  
local m_package_cpath = package.cpath
package.path = string.format("%s;%s?.lua",m_package_path, p)  
package.cpath = string.format("%s;%s?.so",m_package_cpath, p)  

local pp = require("pp")
local parser = require("parse_rpc")

function deal_parse_result(dict, filename)
	local all_class = {}
	local all_function = {}
	local all_outputs = {}
	for _, t in pairs(dict) do
		if t.type == "class" then
			all_class[t.name] = t.value
		elseif t.type == "function" then
			all_function[t.name] = t.value
		end
	end
	check_class(all_class, filename)
	check_func(all_function, all_class, filename)
	return all_class, all_function
end


function parse_file(filename)
	print("-----------"..filename.."--------------")
	local parser_res = parser.parse_file(filename)
	local clstbl,functbl = deal_parse_result(parser_res, filename)
	print("---- class: " .. table.show(clstbl))
	print("---- function: " .. table.show(functbl))
end

function translate_one(all_functions, all_classes, all_modules, result, imp_module)
	for _, t in ipairs(result) do
		if imp_module then
			t.module, _ = string.gsub(imp_module, "%.", "/")
			t.c_imp =  imp_module == "c" and "true" or "false"
			all_modules[t.module] = true
		else
			t.module = "no_such_module"
		end
		if t.type == "function" then
			table.insert(all_functions, t)
		elseif t.type == "class" then
			table.insert(all_classes, t)
		elseif t.type == "implement" then
			translate_one(all_functions, all_classes, all_modules, t.declare, t.imp_module)
		end
	end
end

function table_index(table, elem)
	for i, v in ipairs(table) do
		if v.name == elem then
			return i - 1
		end
	end
	return -1
end

local type_2_value_meta = {
    ['bool'] = 0,
    ['int'] = 0,
    ['string'] = 1,
    ['class'] = 2,
    ['object'] = 3,
    ['mixed'] = 4,
    ['buffer'] = 5,
    ['int8'] = 6,
    ['int16'] = 7,
--    ['float'] = 8,
}

function parse_type(cls_table, ...)
	local arg = {...}
	local cls_index = table_index(cls_table, arg[1])
	local field_type = arg[1]
	if cls_index >= 0 then
		field_type = "class"
        field_type_value = nil
    else
        field_type_value = transfer_type_2_value(field_type)
	end
	return field_type, type_2_value_meta[field_type], cls_index, ((arg[2] == "*") and -1 or -2)
end

--class : value= {1= {name=key,type= {1=string,2=*,},},2= {name=value,type= {1=int,},},},type=class,name=equip_value_t,
--class : value= {1= {name=qianghuaCnt,type= {1=int,2=*,},},2= {name=qianghuaAddRate,type= {1=int,},},3= {name=qianghuaMaxCnt,type= {1=int,},},},type=class,name=equip_qianghua_t,

local type_2_c_struct_meta = {
    ['int'] = 'int',
    ['string'] = 'fs_rpc_string_t', 
    ['int16'] = 'fs_rpc_int16_t',
    ['int8'] = 'fs_rpc_int8_t',
--[[
    ['float'] = 'float',
	['class'] = 2,
	['object'] = 3,
	['mixed'] = 4,
	['buffer'] = 5,
	['bool'] = 0,
--]]
}

function transfer_type_2_value(field_type)
	local field_type_value = type_2_value_meta[field_type]
	if field_type_value == nil then
		error("type error with value ["..field_type.."]")
	end
	return field_type_value
end

function transfer_type_2_c_struct(field_type, ...)
	if arg[2] == "*" then
		return "fs_rpc_array_t";
	end
	if field_type == "class" then
		return "struct "..arg[1]
	end
	local field_type_value = type_2_c_struct_meta[field_type]
	if field_type_value == nil then
		error("type error with value ["..field_type.."]")
	end
	return field_type_value
end

function cls_trans(fl, all_cls_table, cls_table)
	local c_imp = (cls_table.c_imp == "true") and 1 or 0
	table.insert(fl, string.format("field_count:%d,c_imp:%d,class_name=%s", #cls_table.value, c_imp, cls_table.name))
	for _, v in ipairs(cls_table.value) do
		local field_name = v.name
		local field_type, field_type_value, class_index, array = parse_type(all_cls_table, unpack(v.type))
		table.insert(fl, string.format("field_type:%d,class_index:%d,array:%d,field_name:%s", 
			field_type_value, class_index, array, field_name))
	end
end

--function : value= {1= {name=user,type= {1=object,},},2= {name=item,type= {1=int,},},3= {name=pos,type= {1=int,},},},type=function,name=rpc_server_unwield_equip,
--function : value= {1= {name=uid,type= {1=int,},},2= {name=itemid,type= {1=int,},},3= {name=type,type= {1=string,},},4= {name=last,type= {1=int,},},5= {name=qianghuaInfo,type= {1=class,2=equip_qianghua_t,},},6= {name=baseAttr,type= {1=class,2=equip_value_t,3=*,},},7= {name=xilianAttr,type= {1=class,2=equip_value_t,3=*,},},8= {name=baoshis,type= {1=string,2=*,},},},type=function,name=rpc_client_equip_item_info,

function func_trans(rpc_c_func_meta_fl, rpc_c_func_decl_fl, fl, all_cls_table, func_table, func_id)
	--print("function : "..table.show(func_table))
	local c_imp = (func_table.c_imp == "true") and 1 or 0
	local modname = func_table.module or ""
	table.insert(fl, string.format("function_id:%d,c_imp:%d,arg_count:%d,module:%s,function_name:%s", 
		func_id, c_imp, #func_table.value, modname, func_table.name))

	local decl_func_args = ""
	for _, v in ipairs(func_table.value) do
		local field_type, field_type_value, class_index, array = parse_type(all_cls_table, unpack(v.type))
		table.insert(fl, string.format("arg_type:%d,class_index:%d,array:%d",
			field_type_value, class_index, array))

		if c_imp == 1 then
			local field_type_c_struct = transfer_type_2_c_struct(field_type, unpack(v.type))
			if #decl_func_args > 0 then
				decl_func_args = decl_func_args..","
			end
			decl_func_args = decl_func_args..field_type_c_struct..(field_type=="class" and "*" or "")
		end
		
	end
	if c_imp == 1 and string.sub(func_table.name, 1, 10) == "rpc_server" then 
		table.insert(rpc_c_func_meta_fl, string.format("{\"%s\", (fs_rpc_c_function_t)%s,},", func_table.name, func_table.name))
		table.insert(rpc_c_func_decl_fl, string.format("void %s(%s);", func_table.name, decl_func_args))
	end
end

function c_struct_trans(rpc_c_struct_meta_fl, fl, rpc_c_struct_name_fl, decl_fl, all_cls_table, cls_table)
	--print("class : "..table.show(cls_table))
	local c_imp = (cls_table.c_imp == "true") and 1 or 0
	if c_imp ~= 1 then 
		return
	end
	table.insert(fl, string.format("\nstruct %s {", cls_table.name))
	table.insert(decl_fl, string.format("\nstatic fs_rpc_field_meta_t %s_fields[] = {", cls_table.name))
	table.insert(rpc_c_struct_meta_fl, string.format("        {\"%s\", sizeof(struct %s), %d, %s_fields,},", 
				cls_table.name, cls_table.name, #cls_table.value, cls_table.name))
	table.insert(rpc_c_struct_name_fl, cls_table.name)
	for _, v in ipairs(cls_table.value) do
		local field_name = v.name
		local field_type, field_type_value, class_index, array = parse_type(all_cls_table, unpack(v.type))
		--print(cls_table.name, table.show(v))
		--print("name = ",_, v, field_type, field_type_value, class_index, array, "end")
		local field_type_c_struct = transfer_type_2_c_struct(field_type, unpack(v.type))
		table.insert(fl, string.format("        %s %s;", field_type_c_struct, field_name))
		table.insert(decl_fl, string.format("        {\"%s\", offsetof(struct %s, %s), },", field_name, cls_table.name, field_name))
	end
	table.insert(fl, "};")
	table.insert(decl_fl, "};")
end

function static_rpc_table(file)
	local tbl = {}
	local static_rpc_table = parser.parse_file(file)
	for _, e in ipairs(static_rpc_table) do
		if e.type == "define" then
			tbl[e.name] = tonumber(e.value)
		end
	end
	return tbl
end


function startswith( str, substr)
    local len = string.len( substr )

    print(str, substr, string.sub(str, 1, len), len, string.sub(str, 1, len) == substr )

    return string.sub(str, 1, len) == substr

end

function translate(parse_result_tbl, input, output)
	local all_functions = {}
	local all_classes = {}
	local rpc_cfg_fl = {}
	local rpc_cfg_fl_client = {}
	local rpc_id_fl = {}
	--local rpc_id_decl_fl = {}
	local rpc_c_decl_fl = {}
	local rpc_c_struct_fl = {}
	local rpc_c_struct_meta_fl = {}
	local rpc_c_func_meta_fl = {}
	local rpc_c_func_decl_fl = {}
	local rpc_c_struct_name_fl = {}
	local rpc_static_begin_pid = 1
	local all_modules = {}

	local rpc_static_pid_tbl = static_rpc_table(input.."static_rpc_id.h")
	for k, v in pairs(old_pid_table) do
		rpc_static_pid_tbl[k] = v
	end
	for _, v in pairs(rpc_static_pid_tbl) do
		if v >= rpc_static_begin_pid then
			rpc_static_begin_pid = v
		end
	end

	for _, t in ipairs(parse_result_tbl) do
		translate_one(all_functions, all_classes, all_modules, t.content)
	end

	-- print(table.show(all_functions))

	table.insert(rpc_cfg_fl, string.format("class_table_num:%d", #all_classes))
	table.insert(rpc_cfg_fl_client, string.format("class_table_num:%d", #all_classes))
	for _, t in ipairs(all_classes) do
		cls_trans(rpc_cfg_fl, all_classes, t)
		cls_trans(rpc_cfg_fl_client, all_classes, t)
		c_struct_trans(rpc_c_struct_meta_fl, rpc_c_struct_fl, rpc_c_struct_name_fl, rpc_c_decl_fl, all_classes, t)
	end

	table.insert(rpc_cfg_fl, string.format("function_table_num:%d", #all_functions))
	local pid_tbl = {}
    local clientPtoCnt = 0
	for i, t in ipairs(all_functions) do
        if startswith(t.name, "rpc_client" ) then
            clientPtoCnt = clientPtoCnt + 1
        end
        if startswith(t.name, "rpc_server" ) then
            clientPtoCnt = clientPtoCnt + 1
        end
		local pid = rpc_static_pid_tbl[string.upper(t.name)]
		if pid == nil then
			rpc_static_begin_pid = rpc_static_begin_pid + 1
			pid = rpc_static_begin_pid 
		end
		func_trans(rpc_c_func_meta_fl, rpc_c_func_decl_fl, rpc_cfg_fl, all_classes, t, pid)
		pid_tbl[pid] = string.upper(t.name)
	end
    print( "clientPtoCnt", clientPtoCnt)
	table.insert(rpc_cfg_fl_client, string.format("function_table_num:%d", clientPtoCnt))
    for i, t in ipairs(all_functions) do
        if startswith(t.name, "rpc_client" ) or startswith(t.name, "rpc_server" ) then
            local pid = rpc_static_pid_tbl[string.upper(t.name)]

            if pid == nil then
                rpc_static_begin_pid = rpc_static_begin_pid + 1
                pid = rpc_static_begin_pid
            end
            func_trans(rpc_c_func_meta_fl, rpc_c_func_decl_fl, rpc_cfg_fl_client, all_classes, t, pid)
        end
    end

	local rpc_meta_fl = {}

	--table.insert(rpc_id_decl_fl, "#import rc.rpc.rpc_meta as Rpc")
	local sorted_pid = {}
	for pid, _ in pairs(pid_tbl) do
		table.insert(sorted_pid, pid)
	end
	table.sort(sorted_pid)
	for _, pid in pairs(sorted_pid) do
		local defname = pid_tbl[pid]
		table.insert(rpc_id_fl, string.format("#define %s %d", defname, pid))
		table.insert(rpc_meta_fl, string.format("\"%s\" : %s,", defname, defname))
		--table.insert(rpc_id_decl_fl, string.format("#define GET_%s Rpc->GetId(\"%s\")", defname, defname))
	end

	-- rpc_meta.c
	table.insert(rpc_meta_fl, 1, "#include \"/rc/rpc/rpc_id.h\"")
	table.insert(rpc_meta_fl, 2, "static mapping data = {")
	table.insert(rpc_meta_fl, "};")
	table.insert(rpc_meta_fl, [[

int GetId(string strId)
{
	return data[strId];
}

static mapping id2str = {};

string GetProtoNameById( int id )
{
	return id2str[id];
}

void create()
{
	foreach( string s, int pid in data )
	{
		id2str[pid] = s;
	}
}


]])
	local rpc_modules_content = table.concat(rpc_meta_fl, "\n")
	sf = io.open(output.."rpc_meta.c", "w")
	sf:write(rpc_modules_content)
	io.close(sf)

	-- rpc.cfg
	local rpc_cfg_content = table.concat(rpc_cfg_fl, "\n")
	sf = io.open(output.."rpc.cfg", "w")
	sf:write(rpc_cfg_content)
	io.close(sf)

    local rpc_cfg_client_content = table.concat(rpc_cfg_fl_client, "\n")
	sf = io.open(output.."_rpc_for_client.cfg", "w")
	sf:write(rpc_cfg_client_content)
	io.close(sf)

	-- rpc_id.h

	--table.insert(rpc_id_fl, 1, "#include <static_rpc_id.h>")
	table.insert(rpc_id_fl, 1, [[ 
#ifndef _FS_RPC_ID_
#define _FS_RPC_ID_
]]);
	table.insert(rpc_id_fl, "\n#endif /*_FS_RPC_ID_*/\n");
	local rpc_id_content = table.concat(rpc_id_fl, "\n")
	sf = io.open(output.."rpc_id.h", "w")
	sf:write(rpc_id_content)
	io.close(sf)


--	-- rpc_id_decl.h
--	table.insert(rpc_id_decl_fl, 1, [[ 
--#ifndef _FS_RPC_ID_DECL_
--#define _FS_RPC_ID_DECL_
--]]);
--	table.insert(rpc_id_decl_fl, "\n#endif /*_FS_RPC_ID_DECL_*/\n");
--	local rpc_id_decl_content = table.concat(rpc_id_decl_fl, "\n")
--	sf = io.open(output.."rpc_id_decl.h", "w")
--	sf:write(rpc_id_decl_content)
--	io.close(sf)


	--fs_rpc_c.h
	local rpc_c_struct_macros_fl = {}
	local rpc_c_struct_typedef_fl = {}
	for i, c_cls_name in ipairs(rpc_c_struct_name_fl) do
		table.insert(rpc_c_struct_macros_fl, string.format("       struct %s * %sp; \\", 
				c_cls_name, c_cls_name))
		table.insert(rpc_c_struct_typedef_fl, string.format("typedef struct %s %s;", c_cls_name, c_cls_name))
	end
	table.insert(rpc_c_struct_macros_fl, 1, "#define FS_RPC_C_TYPE \\")
	table.insert(rpc_c_struct_macros_fl, 2, "       void *data;     \\")
	table.insert(rpc_c_struct_macros_fl, 3, "       fs_rpc_int_t *intp;     \\")
	table.insert(rpc_c_struct_macros_fl, 4, "       fs_rpc_string_t *stringp;       \\")
	table.insert(rpc_c_struct_macros_fl, "\n")
	table.insert(rpc_c_struct_fl, 1, [[
#ifndef _FS_RPC_C_H
#define _FS_RPC_C_H
#include "fs_rpc.h"
#include "fs_rpc_id.h"
extern fs_rpc_class_meta_t fs_rpc_class_metas[];
extern fs_rpc_function_meta_t fs_rpc_function_metas[];

typedef struct fs_rpc_array_s fs_rpc_array_t;
]])
	table.insert(rpc_c_struct_fl, 2, table.concat(rpc_c_struct_typedef_fl, "\n"))
	table.insert(rpc_c_struct_fl, 3, table.concat(rpc_c_struct_macros_fl, "\n"))
	table.insert(rpc_c_struct_fl, 4, [[
struct fs_rpc_array_s {;
        fs_rpc_size_t n;
        union {
        FS_RPC_C_TYPE
        }u;
};]])
	table.insert(rpc_c_struct_fl, [[#endif /*_FS_RPC_C_H*/]])
	local c_struct_content = table.concat(rpc_c_struct_fl, "\n")
	sf = io.open(output.."fs_rpc_c.h", "w")
	sf:write(c_struct_content)
	io.close(sf)

	--rpc_c.c
	table.insert(rpc_c_decl_fl, 1, "#include \"fs_rpc_c.h\"")
	table.insert(rpc_c_struct_meta_fl, 1, "\nfs_rpc_class_meta_t fs_rpc_class_metas[] = {")
	table.insert(rpc_c_struct_meta_fl, "};\n")
	table.insert(rpc_c_struct_meta_fl, table.concat(rpc_c_func_decl_fl, "\n"))
	table.insert(rpc_c_func_meta_fl, 1, "\nfs_rpc_function_meta_t fs_rpc_function_metas[] = {")
	table.insert(rpc_c_func_meta_fl, "{NULL, NULL,},")
	table.insert(rpc_c_func_meta_fl, "};\n")
	local c_struct_decl_content = table.concat(rpc_c_decl_fl, "\n")..table.concat(rpc_c_struct_meta_fl, "\n").."\n"..table.concat(rpc_c_func_meta_fl, "\n")
	sf = io.open(output.."rpc_c.c", "w")
	sf:write(c_struct_decl_content)
	io.close(sf)
end



local output_dir = arg[1]

if output_dir == nil then
	print("please input an absolubte path of script")
	os.exit(-1)
end

if string.sub(output_dir, #output_dir, #output_dir) ~= "/" then
	output_dir = output_dir.."/"
end



local input = output_dir.."rc/rpc_decl/"
local temp_output = output_dir.."tools/makerpc/output/"

--local static_rpc_table = parser.parse_file(input.."static_rpc_id.h") 
--print(table.show(static_rpc_table))
--print(parser.server_file_lpc_serial(result, "scene.h"))
--translate({[1] = {["content"] = result, ["file"] = "scene.h" } }, temp_output)

----[[
local result = parser.parse_dir(input) 
local engine_dir = output_dir.."../engine/packages/"
local script_dir = output_dir.."rc/rpc/"
local v_script_dir = output_dir.."rc/rpc_client/"
--print(table.show(result))
-- 清理干净目标目录
local old_rpc_id_filename = script_dir.."rpc_id.h"
if io.open(old_rpc_id_filename, "r") ~= nil then
	os.execute("sed -i -e '1,4d;$d' "..old_rpc_id_filename)
	old_pid_table = static_rpc_table(script_dir.."rpc_id.h")
else
	--old_pid_table = {}
    old_pid_table = static_rpc_table(input.."static_rpc_id.h")
end

os.execute("rm "..script_dir.."*.h")
os.execute("rm "..script_dir.."*.c")
os.execute("rm "..v_script_dir.."*.h")

translate(result, input, temp_output)

for _, t in ipairs(result) do
	local file_name, _ = string.gsub(t.file, ".decl", ".h")
	--print("file_name", t.file, file_name, t.content, script_dir..file_name)

	local content = parser.server_file_lpc_serial(t.content, file_name)
	sf = io.open(script_dir..file_name, "w")
	sf:write(content)
	io.close(sf)

	local v_file_name = "v_"..file_name
	content = parser.client_file_lpc_serial(t.content, v_file_name)
	sf = io.open(v_script_dir..file_name, "w")
	sf:write(content)
	io.close(sf)
end

os.execute("mv "..temp_output.."rpc_c.c "..engine_dir.."/")
os.execute("mv "..temp_output.."fs_rpc_c.h "..engine_dir.."/")
--os.execute("cp "..output_dir.."include/static_rpc_id.h "..engine_dir.."/static_rpc_id.h")
os.execute("cp "..temp_output.."rpc_id.h "..engine_dir.."/fs_rpc_id.h")
os.execute("mv "..temp_output.."rpc_id.h "..script_dir.."/")
os.execute("mv "..temp_output.."rpc_meta.c "..script_dir.."/")
--os.execute("mv "..temp_output.."rpc_id_decl.h "..script_dir.."/")
os.execute("mv "..temp_output.."rpc.cfg "..script_dir.."/")
os.execute("mv "..temp_output.."_rpc_for_client.cfg "..script_dir.."/")

----]]

print("parse ok")

