from xml.sax import saxutils as su
import markdown
from jinja2 import Template
import datetime
from textwrap import dedent

import imp

import os

tool_xml = """<?xml version="1.0"?>
<metadata xml:lang="en">
	<Esri>
		<CreaDate>{{current_date}}</CreaDate>
		<CreaTime>{{current_time}}</CreaTime>
		<ArcGISFormat>1.0</ArcGISFormat>
		<SyncOnce>TRUE</SyncOnce>
		<ModDate>{{current_date}}</ModDate>
		<ModTime>{{current_time}}</ModTime>
		<scaleRange>
			<minScale>150000000</minScale>
			<maxScale>5000</maxScale>
		</scaleRange>
	</Esri>
	
	<tool name="{{tool.name}}" displayname="{{tool.displayname}}" toolboxalias="{{tool.toolboxalias}}" xmlns="">
	<parameters>
    {% for param in params -%}
	<param name="{{param.param_name}}" displayname="{{param.param_display_name}}" type="{{param.param_type}}" direction="{{param.param_direction}}" datatype="{{param.data_type}}" expression="{{param.param_expression}}">
	{% if param.dialog_reference -%}
		<dialogReference>{{param.dialog_reference}}</dialogReference>
	{% endif %}
	{%- if param.python_reference -%}
		<pythonReference>{{param.python_reference}}</pythonReference>
	{% endif %}
	</param>
	{% endfor %}
	</parameters>
	{% if tool.summary -%}
		<summary>{{tool.summary}}</summary>
	{% endif %}
	{%- if tool.usage -%}
		<usage>{{tool.usage}}</usage>
	{% endif %}
    </tool>
	<dataIdInfo>
		<idCitation>
			<resTitle>tool.displayname</resTitle>
		</idCitation>
		<searchKeys>
			{%- if tool.tags -%}
			{% for tag in tool.tags %}<keyword>{{tag}}</keyword>
			{% endfor %}{% endif %}
		</searchKeys>
        <idCredit></idCredit>
        <resConst>
            <Consts>
                <useLimit></useLimit>
            </Consts>
        </resConst>
	</dataIdInfo>

	<distInfo>
		<distributor>
			<distorFormat>
				<formatName>ArcToolbox Tool</formatName>
			</distorFormat>
		</distributor>
	</distInfo>
	<mdHrLv>
		<ScopeCd value="005"/>
	</mdHrLv>
</metadata>"""

def meta_toolbox(toolbox_path):
    input_file = toolbox_path
    toolbox_source = imp.load_source(
        "working_tbx", input_file)

    tbx = toolbox_source.Toolbox()
    for _tool in tbx.tools:
        _tool = _tool()
        process_tool(toolbox_path, tbx, _tool)

def process_tool(toolbox_path, toolbox, tool):
    tool_data = build_xml_data(toolbox, tool)
    save_xml_file(toolbox_path, tool_data, toolbox, tool)

def build_tool_data(toolbox, tool):
    meta_params = tool.meta_params if hasattr(tool, 'meta_params') else {}
    summary = meta_params.get('summary', None)
    usage = meta_params.get('usage', None)
    tool_data = {
        'name': tool.__class__.__name__,
        'displayname': tool.label if hasattr(tool, 'label') else '',
        'toolboxalias': toolbox.__class__.__name__,
        'xmlns': '',
        'tags': meta_params.get('tags', [])
    }

    if summary:
        tool_data['summary'] = markdown_data(summary)
    if usage:
        tool_data['usage'] = markdown_data(usage)

    return tool_data

def build_parameter_data(tool):
    param_list = []
    meta_params = tool.meta_params if hasattr(tool, 'meta_params') else {}
    for parameter in tool.getParameterInfo():
        tool_meta = meta_params.get(parameter.name, {})
        diag_ref = tool_meta.get('dialog_reference', None)
        py_ref = tool_meta.get('python_reference', None)

        pr = {
            "param_name": parameter.name,
            "param_display_name": parameter.displayName,
            "param_type": parameter.parameterType,
            "param_direction": parameter.direction,
            "data_type": parameter.datatype,
            "param_expression": parameter.name,
        }

        if diag_ref:
            pr["dialog_reference"] = markdown_data(diag_ref)
        if py_ref:
            pr["python_reference"] = markdown_data(py_ref)

        param_list.append(pr)

    return param_list

def parse_to_xml(tool_dict, param_dict, current_date, current_time):
    _template = Template(tool_xml)
    _rendered = _template.render(tool=tool_dict, params=param_dict, current_date=current_date, current_time=current_time)
    return _rendered

def wrap_div(content):
    return '<DIV STYLE="text-align:Left;"><DIV><P><SPAN>{}</SPAN></P></DIV></DIV>'.format(content)

def build_xml_data(tbx, _tool):
    t_data = build_tool_data(tbx, _tool)
    p_data = build_parameter_data(_tool)
    _current_datetime = datetime.datetime.now()
    current_date = _current_datetime.strftime("%Y%m%d")
    current_time = _current_datetime.strftime("%H%M%S00")

    xml_data = parse_to_xml(t_data, p_data, current_date, current_time)

    return xml_data

def save_xml_file(toolbox_path, xml_data, toolbox, tool, **kwargs):
    toolbox_folder = "\\".join(toolbox_path.split("\\")[:-1])
    toolbox = toolbox_path.split("\\")[-1].replace(".pyt", "")
    fname = os.path.join(toolbox_folder, "{}{}.{}.pyt.xml".format(kwargs.get("prefix",""), toolbox, tool.__class__.__name__))
    with open(fname, 'w') as f:
        f.write(xml_data)

def markdown_data(text):
    new_text = dedent(text)
    new_text_md = markdown.markdown(new_text)
    return su.escape(new_text_md)
