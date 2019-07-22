# Usage: execute
# $ python support/generate.py
# at wpt/upgrade-insecure-requests/.
#
# Note: Some tests (link-upgrade.sub.https.html and
# websocket-upgrade.https.html) are not covered by this generator script.

template = '''<!DOCTYPE html>
<html>
<head>
<!-- Generated by wpt/upgrade-insecure-requests/support/generate.py -->%(additionalMeta)s
<title>Upgrade Insecure Requests: %(name)s.</title>
<script src="/resources/testharness.js"></script>
<script src="/resources/testharnessreport.js"></script>
<script src="./support/testharness-helper.sub.js"></script>
<script src="/common/security-features/resources/common.js"></script>

<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
</head>
<body>
<script>
const tests = %(generatorName)s(ResourceType.%(resourceType)s, %(sameOriginOnly)s);
tests.forEach(test => testMap['%(name)s'](test));
</script>
</body>
</html>
'''

def getLong(file):
  testsThatNeedMoreTime = [ "worker-subresource-fetch-redirect-upgrade.https.html" ]
  if any(file in item for item in testsThatNeedMoreTime ):
    return '\n<meta name="timeout" content="long">'
  return ""

# resourceType is |ResourceType| in testharness-helper.sub.js.
for name, resourceType in [
  ('image', 'IMAGE'), ('iframe', 'FRAME'),
  ('animation-worklet', 'WORKLET'), ('audio-worklet', 'WORKLET'),
  ('layout-worklet', 'WORKLET'), ('paint-worklet', 'WORKLET'),
  ('worker', 'WORKER'),
  ('module-worker', 'WORKER'),
  ('worker-subresource-xhr', 'FETCH'),
  ('worker-subresource-fetch', 'FETCH')]:
  sameOriginOnly = 'true' if resourceType == 'WORKER' else 'false'
  types = [('', 'generateTests'), ('-redirect', 'generateRedirectTests')]
  if name == 'module-worker' or resourceType == 'WORKLET':
    types.append(('-import', 'generateModuleImportTests'))
  for typeName, generatorName in types:
    filename = '%s%s-upgrade.https.html' % (name, typeName)
    with open(filename, 'w') as html_file:
      html_file.write(template % {
          'name': name,
          'additionalMeta': getLong(filename),
          'resourceType': resourceType,
          'generatorName': generatorName,
          'sameOriginOnly': sameOriginOnly})
