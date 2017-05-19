
#include <system_config.h>

int main()
{
	string cDirName = "";
	string cFileName, cDestName, cmd_script;

	string cSvnPath = "https://192.168.0.3/qtz/fs/design/data/building";
	cDestName = __LIB_PATH__ + "/tmp/building/";
	cmd_script = "/tools/svnco.lua";

	os_command("/tools/svnco.sh", cSvnPath + " " + cDestName, "sh");

	cFileName = __LIB_PATH__ + "/tmp/building/5025.lua";
	cDestName = __LIB_PATH__ + "/module/home/data/home_courtyard_zone_cfg.c";
	cmd_script = "/tools/makehome.lua";
	os_command(cmd_script, cFileName + " " + cDestName, "lua");

	cFileName = __LIB_PATH__ + "/tmp/building/5015.lua";
	cDestName = __LIB_PATH__ + "/module/home/data/home_house_zone_cfg.c";
	cmd_script = "/tools/makehome.lua";
	os_command(cmd_script, cFileName + " " + cDestName, "lua");

	cFileName = __LIB_PATH__ + "/tmp/building/building.lua";
	cDestName = __LIB_PATH__ + "/module/home/data/home_building_range.c";
	cmd_script = "/tools/makehome.lua";
	os_command(cmd_script, cFileName + " " + cDestName, "lua");


	// TODO: update
	cDirName = __LIB_PATH__ + "/tmp/building/group/";
	cDestName = __LIB_PATH__ + "/module/home/data/home_building_group.c";
	cmd_script = "/tools/makehome.lua";
	os_command(cmd_script, cDirName + " " + cDestName, "lua");

	return 0;
}
