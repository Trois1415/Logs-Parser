import os
os.system('cls')
#Parsing script

file = input("Log file location : ")
with open(file, 'r') as f:
	file = f.readlines()
	tab_file = [line for line in file]

#scrapped_line_file = [Domain, Timestamp, Request, HTTPResponse, Size]
scraped_lines_file = [[
					  line[0:line.find(" - -")],
					  line[line.find("[")+1:line.find("]")],
					  line[line.find(' "')+2:line.find('" ')],
					  line[line.find('" ')+2:line.find('" ')+5],
					  line[line.find('" ')+6:-1]
					  ]
					  for line in tab_file]

def classify_responses(file):
	responses = {
	    100: [('Continue', 'Request received, please continue'), 0],
	    101: [('Switching Protocols',
	          'Switching to new protocol; obey Upgrade header'), 0],

	    200: [('OK', 'Request fulfilled, document follows'), 0],
	    201: [('Created', 'Document created, URL follows'), 0],
	    202: [('Accepted',
	          'Request accepted, processing continues off-line'), 0],
	    203: [('Non-Authoritative Information', 'Request fulfilled from cache'), 0],
	    204: [('No Content', 'Request fulfilled, nothing follows'), 0],
	    205: [('Reset Content', 'Clear input form for further input.'), 0],
	    206: [('Partial Content', 'Partial content follows.'), 0],

	    300: [('Multiple Choices',
	          'Object has several resources -- see URI list'), 0],
	    301: [('Moved Permanently', 'Object moved permanently -- see URI list'), 0],
	    302: [('Found', 'Object moved temporarily -- see URI list'), 0],
	    303: [('See Other', 'Object moved -- see Method and URL list'), 0],
	    304: [('Not Modified',
	          'Document has not changed since given time'), 0],
	    305: [('Use Proxy',
	          'You must use proxy specified in Location to access this '
	          'resource.'), 0],
	    307: [('Temporary Redirect',
	          'Object moved temporarily -- see URI list'), 0],

	    400: [('Bad Request',
	          'Bad request syntax or unsupported method'), 0],
	    401: [('Unauthorized',
	          'No permission -- see authorization schemes'), 0],
	    402: [('Payment Required',
	          'No payment -- see charging schemes'), 0],
	    403: [('Forbidden',
	          'Request forbidden -- authorization will not help'), 0],
	    404: [('Not Found', 'Nothing matches the given URI'), 0],
	    405: [('Method Not Allowed',
	          'Specified method is invalid for this server.'), 0],
	    406: [('Not Acceptable', 'URI not available in preferred format.'), 0],
	    407: [('Proxy Authentication Required', 'You must authenticate with '
	          'this proxy before proceeding.'), 0],
	    408: [('Request Timeout', 'Request timed out; try again later.'), 0],
	    409: [('Conflict', 'Request conflict.'), 0],
	    410: [('Gone',
	          'URI no longer exists and has been permanently removed.'), 0],
	    411: [('Length Required', 'Client must specify Content-Length.'), 0],
	    412: [('Precondition Failed', 'Precondition in headers is false.'), 0],
	    413: [('Request Entity Too Large', 'Entity is too large.'), 0],
	    414: [('Request-URI Too Long', 'URI is too long.'), 0],
	    415: [('Unsupported Media Type', 'Entity body in unsupported format.'), 0],
	    416: [('Requested Range Not Satisfiable',
	          'Cannot satisfy request range.'), 0],
	    417: [('Expectation Failed',
	          'Expect condition could not be satisfied.'), 0],

	    500: [('Internal Server Error', 'Server got itself in trouble'), 0],
	    501: [('Not Implemented',
	          'Server does not support this operation'), 0],
	    502: [('Bad Gateway', 'Invalid responses from another server/proxy.'), 0],
	    503: [('Service Unavailable',
	          'The server cannot process the request due to a high load'), 0],
	    504: [('Gateway Timeout',
	          'The gateway server did not receive a timely response'), 0],
	    505: [('HTTP Version Not Supported', 'Cannot fulfill request.'), 0],
	    }

	for line in file:
		responses[int(line[3])][1] += 1

	informational_responses = 0
	for i in range(2):
		informational_responses += responses[100+i][1]

	print(f"{informational_responses} informational responses found including :")
	for i in range(2):
		print(f"    {responses[100+i][1]} {responses[100+i][0][0]}")

	success = 0
	for i in range(7):
		success += responses[200+i][1]

	print(f"{success} success found including :")
	for i in range(7):
		print(f"    {responses[200+i][1]} {responses[200+i][0][0]}")

	redirections = 0
	for i in range(8):
		if 300+i == 306:	continue
		redirections += responses[300+i][1]

	print(f"{redirections} redirections found including :")
	for i in range(8):
		if 300+i == 306:	continue
		print(f"    {responses[300+i][1]} {responses[300+i][0][0]}")

	client_errors = 0
	for i in range(18):
		client_errors += responses[400+i][1]

	print(f"{client_errors} client errors found including :")
	for i in range(18):
		print(f"    {responses[400+i][1]} {responses[400+i][0][0]}")

	server_errors = 0
	for i in range(6):
		server_errors += responses[500+i][1]

	print(f"{server_errors} server errors found including :")
	for i in range(6):
		print(f"    {responses[500+i][1]} {responses[500+i][0][0]}")



print(f"{len(scraped_lines_file)} requests found.")
input("Press any key to show HTTPResponse...")
os.system('cls')
classify_responses(scraped_lines_file)

#domains -> dict{domains : [requests, total_size]}
domains = {}
for line in scraped_lines_file:
	dom = line[0]
	size = line[4]
	try:
		x = domains.get(dom)
		domains[dom][0] += 1
		if size != '-':
			domains[dom][1] += int(size)
	except KeyError:
		domains.setdefault(dom, [0, 0])

input("Press any key to show Occurences...")
os.system('cls')
shown = 0
req = int(input("Minimum : "))
for domain in domains:
	if domains.get(domain)[0] > req:
		print(f"{domain} request {domains.get(domain)[0]} times.")
		shown += 1

if shown == 0:
	print(f"No domain has made more than {req} requests")

domains_list = list(domains.keys())
domain_max = domains_list[0]
size_max = domains[domain_max][1]
for i in range(1, len(domains_list)):
	if domains[domains_list[i]][1] > size_max:
		size_max = domains[domains_list[i]][1]
		domain_max = domains_list[i]

print("\n")
print(f"{domain_max} receive the more bytes ({size_max} bytes)")


input("Press any key to show information about a page...")
os.system('cls')
page = input("Page : ")
scrap_page = [i for i in range(len(scraped_lines_file)) if scraped_lines_file[i][2][4:4+len(page)] == page]

print("\n")
print(f"{len(scrap_page)} requests leads to {page}")

page_only_log = [scraped_lines_file[index] for index in scrap_page]

classify_responses(page_only_log)