import re, sys, os

def renpy_to_dot(script_lines):
    dot_lines = ["digraph RenPyFlow {"]

    label_pattern = re.compile(r"label\s+(\w+):")
    jump_pattern = re.compile(r"jumb\s+(\w+)|jump\s+(\w+)")
    menu_pattern = re.compile(r"menu\s+(\w+):")
#    choice_pattern = re.compile(r'"(.+)"\s*:\s*\n\s*jump\s+(\w+)')
#    choice_pattern = re.compile(r'"(.+)"\s*:\s*')
    choice_pattern = re.compile(r'"(?:.+)}(.+)\s\\n{(?:.+)":')
    choice_pattern1 = re.compile(r'"(?:.+)}(.+)":')
    if_pattern = re.compile(r"if\s+(.+):")
    else_pattern = re.compile(r"else:")

    current_label = None
    current_menu = None
    pending_vars = []
    last_if_clause = None
    awaiting_else = 0
    if_no = 0
    
    ######################
    restore_label = []
    ######################

    for line in script_lines:
        line = line.strip()

        # Detect label
        label_match = label_pattern.match(line)
        if label_match:
            lbl = label_match.group(1)
            dot_lines.append(f'    {lbl} [shape=box];')
            # If this label comes after an if/else, connect it
#            if last_if_clause and not awaiting_else:
#                dot_lines.append(f'    {current_label} -> {lbl} [label="Yes"];')
 #               last_if_clause = None
#            elif last_if_clause and awaiting_else:
#                dot_lines.append(f'    {current_label} -> {lbl} [label="No"];')
#                last_if_clause = None
#                awaiting_else = False
            current_label = lbl
            continue

        # Variable assignment
        if line.startswith("$"):
            expr = line[1:].strip()
            pending_vars.append(expr)
            continue

        # Jump
        print(current_label)
        jump_match = jump_pattern.match(line)
        if jump_match and current_label:
            target = jump_match.group(1) or jump_match.group(2)
            if pending_vars:
                html_lines = []
                for expr in pending_vars:
                    if any(tok in expr for tok in ["==", "!=", "True", "False"]):
                        html_lines.append(f'<TR><TD><FONT COLOR="red">{expr}</FONT></TD></TR>')
                    else:
                        html_lines.append(f'<TR><TD><FONT COLOR="black">{expr}</FONT></TD></TR>')
                html_label = "<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\">" + "".join(html_lines) + "</TABLE>"
                dot_lines.append(f'    {current_label} -> {target} [label=<{html_label}>];')
                pending_vars.clear()
            else:
                dot_lines.append(f'    {current_label} -> {target};')
            dot_lines.append(f'    {target} [shape=box];')
            

            continue

        # If clause
        if_match = if_pattern.match(line)
        if if_match and current_label:
            condition = if_match.group(1)
            last_if_clause = f"if_clause{if_no}"
            if_no += 1
            if pending_vars:
                html_lines = []
                for expr in pending_vars:
                    if any(tok in expr for tok in ["==", "!=", "True", "False"]):
                        html_lines.append(f'<TR><TD><FONT COLOR="red">{expr}</FONT></TD></TR>')
                    else:
                        html_lines.append(f'<TR><TD><FONT COLOR="black">{expr}</FONT></TD></TR>')
                html_label = "<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\">" + "".join(html_lines) + "</TABLE>"
                dot_lines.append(f'    {current_label} -> {last_if_clause} [label=<{html_label}>];')
                pending_vars.clear()
            else:    
                dot_lines.append(f'    {current_label} -> {last_if_clause};')
            dot_lines.append(f'    {last_if_clause} [shape=diamond, label="{condition}"];')
            pending_vars.append("Yes")
            restore_label.append(last_if_clause)
            print(restore_label)
            current_label = last_if_clause
            continue

        # Else clause
        if else_pattern.match(line) and last_if_clause:
 #           last_else =if_clause_{if_no}
            awaiting_else += 1
            pending_vars.append("No")
            ################################
            if len(restore_label) != 0 and awaiting_else != 0:
                restore_length = len(restore_label)
                current_label = restore_label.pop(restore_length-1)
                
                awaiting_else -= 1            
            ################################
            #current_label = last_if_clause
            continue

        # Menu
        menu_match = menu_pattern.match(line)
        if menu_match:
            current_menu = menu_match.group(1)
            dot_lines.append(f'    {current_menu} [shape=box, style=filled, color=blue];')
#            if current_label:
 #               dot_lines.append(f'    {current_label} -> {current_menu};')
            if pending_vars:
                html_lines = []
                for expr in pending_vars:
                    if any(tok in expr for tok in ["==", "!=", "True", "False"]):
                        html_lines.append(f'<TR><TD><FONT COLOR="red">{expr}</FONT></TD></TR>')
                    else:
                        html_lines.append(f'<TR><TD><FONT COLOR="black">{expr}</FONT></TD></TR>')
                html_label = "<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\">" + "".join(html_lines) + "</TABLE>"
                dot_lines.append(f'    {current_label} -> {current_menu} [label=<{html_label}>];')
                pending_vars.clear()
            else:
                dot_lines.append(f'    {current_label} -> {current_menu};')

            current_label = current_menu
            continue

        # Menu choices
        choice_match = choice_pattern.match(line)
        #choice_text = choice_match.group(1)
#        if choice_match:
#            if not choice_match.group(1):
#                choice_match = choice_pattern1.match(line)
                #choice_text = choice_match.group(1)
        if choice_match and current_menu:
            #choice_text, target = choice_match.groups()
            #dot_lines.append(f'    {current_menu} -> {target} [label="{choice_text}"];')
            #dot_lines.append(f'    {target} [shape=box];')
            choice_text = choice_match.group(1)
            #print(choice_text)
            if choice_text:
                pending_vars.append(choice_text)
            continue
        
        choice_match1 = choice_pattern1.match(line)
        if choice_match1 and current_menu:
            #choice_text, target = choice_match.groups()
            #dot_lines.append(f'    {current_menu} -> {target} [label="{choice_text}"];')
            #dot_lines.append(f'    {target} [shape=box];')
            choice_text = choice_match1.group(1)
            #print(choice_text)
            if choice_text:
                pending_vars.append(choice_text)
            continue

    dot_lines.append("}")
    return "\n".join(dot_lines)


# Example usage
#script = [
#    "label a:",
#    "    $ ram += 2",
#    "    $ summer = True",
#    "    jumb b",
#    "label b:",
#    "    menu c:",
#    '    "say d": jump d',
#    '    "say e": jump e',
#    "label e:",
#    "    if shyam >= 10:",
#    "        label f:",
#    "    else:",
#    "        label g:",
#]

# -------- File I/O wrapper --------
def convert_file(input_file, output_dir):
    with open(input_file, "r", encoding="utf-8") as f:
        script_lines = f.readlines()

    dot_code = renpy_to_dot(script_lines)

    base = os.path.basename(input_file).replace(".rpy",".dot")
    with open(os.path.join(output_dir,base), "w", encoding="utf-8") as f:
        f.write(dot_code)

    print(f"DOT code written to {base}")

def main(input_dir,output_dir):
  for file in os.listdir(input_dir):
    if file.endswith(".rpy"):
      convert_file(os.path.join(input_dir,file),output_dir)

if __name__ == "__main__":
  main(sys.argv[1],sys.argv[2])
