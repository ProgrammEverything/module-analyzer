import inspect
# Function to extract and format docstrings and function signatures
def extract_docstrings(module):
    docstrings = {}
    
    # Extract class docstrings
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            docstrings[name] = {
                'doc': obj.__doc__,
                'methods': []
            }
            for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                method_signature = inspect.signature(method)
                method_doc = {
                    'name': method_name,
                    'doc': method.__doc__,
                    'signature': str(method_signature),
                    'args': []
                }
                for param in method_signature.parameters.values():
                    annotation = param.annotation if param.annotation != inspect._empty else "Any"
                    method_doc['args'].append({
                        'name': param.name,
                        'type': annotation,
                        'default': param.default if param.default != param.empty else None
                    })
                docstrings[name]['methods'].append(method_doc)
    
    # Extract function docstrings
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            function_signature = inspect.signature(obj)
            function_doc = {
                'name': name,
                'doc': obj.__doc__,
                'signature': str(function_signature),
                'args': []
            }
            for param in function_signature.parameters.values():
                annotation = param.annotation if param.annotation != inspect._empty else "Any"
                function_doc['args'].append({
                    'name': param.name,
                    'type': annotation,
                    'default': param.default if param.default != param.empty else None
                })
            docstrings[name] = function_doc
    
    return docstrings
import mymodule # Your module which you want to document
file = ""
D_CHAR = "-"
docstrings = extract_docstrings(mymodule)
pages: dict[str,str] = {}
scope = 1
for x,i in docstrings.items():
    tmp = "```\n"
    tmp += scope * 3 * D_CHAR + "CLASS " + x + "\n"
    if i["doc"] != None:
        tmp += i["doc"] + "\n"
    else:
        tmp += scope * 3 * D_CHAR + "No documentation found" + "\n"
    # Structure search
    for doc in i["methods"]:
        tmp += D_CHAR * 3 * scope + "Function: " + str(doc["name"]) + str(doc["signature"]) + "\n"
        scope += 1

        for arg in doc["args"]:
            tmp += f"{D_CHAR * 3 * scope}{arg["name"]}: {arg["type"]} {f"= {arg["default"]}" if arg["default"] != None else "NODEFAULT"}\n"
        tmp += D_CHAR * 3 * scope + (str(doc["doc"]) if doc["doc"] != None else "No documentation found") + "\n"
        scope -= 1
    tmp+="\n```\n"
    pages.update({x : tmp})
for name,content in pages.items():
    print("Page", name)
    print(f"Content:\n{content}")