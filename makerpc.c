
#include <system_config.h>

int main()
{
#if 0
	// rpc描述结果文件,注意，是系统的路径，所以不能是 "/" 打头
	string sys_rpc_cfg = "/rc/config"->GetConfig(RPC_CFG);
	string sys_rpc_id = "rc/rpc/rpc_id.h";
	string rpc_declare = "/rc/rpc_decl/declare.c";
	string rpc_tr_script = "/tools/rpc_tr.sh";
	string output = "./rc/rpc/";
	mapping * decls;
	decls = rpc_declare->get_cfg();
	fs_rpc_make_cfg(decls, sys_rpc_id, sys_rpc_cfg);
	os_command(rpc_tr_script, "" + output, "sh");
#else
	string rpc_parse_script = "/tools/makerpc/to_lpc.lua";
	os_command(rpc_parse_script, __LIB_PATH__, "lua");
	os_command("/tools/rpc2json.py", __LIB_PATH__, "python");
#endif

	return 0;
}
