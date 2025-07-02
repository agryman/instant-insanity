# Arthur's Notes on Google Text-to-Speech

## 2025-07-01

Still trying to test Google text-to-speech.
* The `gcloud init` command mostly worked but failed to create
a default `.boto` file which I believe is used by the Python
client library. 
* The `gsutil config -n` command failed because it required Python 3.12
and my system default is Python 3.13 which I installed using `brew`
```shell
% gsutil config -n


Updates are available for some Google Cloud CLI components.  To install them,
please run:
  $ gcloud components update

Error: gsutil requires Python version 3.8-3.12, but a different version is installed.
You are currently running Python 3.13
Follow the steps below to resolve this issue:
	1. Switch to Python 3.8-3.12 using your Python version manager or install an appropriate version.
	2. If you are unsure how to manage Python versions, visit [https://cloud.google.com/storage/docs/gsutil_install#specifications] for detailed instructions.

```
* my efforts to temporarily unlink Python 3.13 and link Python 3.12
using brew failed, so I reverted to Python 3.13.
```
% python3 --version
Python 3.13.3
```
### pyenv

I believe that the recommended may to manage Python versions is
to use the `pyenv` command which I can install using `brew`

This webpage describes how to manage Python versions:
https://www.askpython.com/python/examples/set-homebrew-default-python-version-macos

I installed `pyenv`:
```shell
brew update
brew install pyenv
```

I initialized `pyenv`:
```shell
% pyenv init
# Load pyenv automatically by appending
# the following to 
# ~/.zprofile (for login shells)
# and ~/.zshrc (for interactive shells) :

export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - zsh)"

# Restart your shell for the changes to take effect.
```

I listed the available versions:
```shell
% pyenv install --list
Available versions:
  2.1.3
  2.2.3
  2.3.7
  2.4.0
  2.4.1
  2.4.2
  2.4.3
  2.4.4
  2.4.5
  2.4.6
  2.5.0
  2.5.1
  2.5.2
  2.5.3
  2.5.4
  2.5.5
  2.5.6
  2.6.0
  2.6.1
  2.6.2
  2.6.3
  2.6.4
  2.6.5
  2.6.6
  2.6.7
  2.6.8
  2.6.9
  2.7.0
  2.7-dev
  2.7.1
  2.7.2
  2.7.3
  2.7.4
  2.7.5
  2.7.6
  2.7.7
  2.7.8
  2.7.9
  2.7.10
  2.7.11
  2.7.12
  2.7.13
  2.7.14
  2.7.15
  2.7.16
  2.7.17
  2.7.18
  3.0.1
  3.1.0
  3.1.1
  3.1.2
  3.1.3
  3.1.4
  3.1.5
  3.2.0
  3.2.1
  3.2.2
  3.2.3
  3.2.4
  3.2.5
  3.2.6
  3.3.0
  3.3.1
  3.3.2
  3.3.3
  3.3.4
  3.3.5
  3.3.6
  3.3.7
  3.4.0
  3.4-dev
  3.4.1
  3.4.2
  3.4.3
  3.4.4
  3.4.5
  3.4.6
  3.4.7
  3.4.8
  3.4.9
  3.4.10
  3.5.0
  3.5-dev
  3.5.1
  3.5.2
  3.5.3
  3.5.4
  3.5.5
  3.5.6
  3.5.7
  3.5.8
  3.5.9
  3.5.10
  3.6.0
  3.6-dev
  3.6.1
  3.6.2
  3.6.3
  3.6.4
  3.6.5
  3.6.6
  3.6.7
  3.6.8
  3.6.9
  3.6.10
  3.6.11
  3.6.12
  3.6.13
  3.6.14
  3.6.15
  3.7.0
  3.7-dev
  3.7.1
  3.7.2
  3.7.3
  3.7.4
  3.7.5
  3.7.6
  3.7.7
  3.7.8
  3.7.9
  3.7.10
  3.7.11
  3.7.12
  3.7.13
  3.7.14
  3.7.15
  3.7.16
  3.7.17
  3.8.0
  3.8-dev
  3.8.1
  3.8.2
  3.8.3
  3.8.4
  3.8.5
  3.8.6
  3.8.7
  3.8.8
  3.8.9
  3.8.10
  3.8.11
  3.8.12
  3.8.13
  3.8.14
  3.8.15
  3.8.16
  3.8.17
  3.8.18
  3.8.19
  3.8.20
  3.9.0
  3.9-dev
  3.9.1
  3.9.2
  3.9.4
  3.9.5
  3.9.6
  3.9.7
  3.9.8
  3.9.9
  3.9.10
  3.9.11
  3.9.12
  3.9.13
  3.9.14
  3.9.15
  3.9.16
  3.9.17
  3.9.18
  3.9.19
  3.9.20
  3.9.21
  3.9.22
  3.9.23
  3.10.0
  3.10-dev
  3.10.1
  3.10.2
  3.10.3
  3.10.4
  3.10.5
  3.10.6
  3.10.7
  3.10.8
  3.10.9
  3.10.10
  3.10.11
  3.10.12
  3.10.13
  3.10.14
  3.10.15
  3.10.16
  3.10.17
  3.10.18
  3.11.0
  3.11-dev
  3.11.1
  3.11.2
  3.11.3
  3.11.4
  3.11.5
  3.11.6
  3.11.7
  3.11.8
  3.11.9
  3.11.10
  3.11.11
  3.11.12
  3.11.13
  3.12.0
  3.12-dev
  3.12.1
  3.12.2
  3.12.3
  3.12.4
  3.12.5
  3.12.6
  3.12.7
  3.12.8
  3.12.9
  3.12.10
  3.12.11
  3.13.0
  3.13.0t
  3.13-dev
  3.13t-dev
  3.13.1
  3.13.1t
  3.13.2
  3.13.2t
  3.13.3
  3.13.3t
  3.13.4
  3.13.4t
  3.13.5
  3.13.5t
  3.14.0b3
  3.14.0b3t
  3.14-dev
  3.14t-dev
  3.15-dev
  3.15t-dev
+ many more Python-adjacent programs such as anaconda, pypi, etc
```
I installed the most recent version of Python 3.12:
```shell
% pyenv install 3.12.11
python-build: use openssl@3 from homebrew
python-build: use readline from homebrew
Downloading Python-3.12.11.tar.xz...
-> https://www.python.org/ftp/python/3.12.11/Python-3.12.11.tar.xz
Installing Python-3.12.11...
python-build: use readline from homebrew
python-build: use zlib from xcode sdk
Installed Python-3.12.11 to /Users/arthurryman/.pyenv/versions/3.12.11
```

Confirm the installation:
```shell
% pyenv versions
* system (set by /Users/arthurryman/.pyenv/version)
  3.12.11
```

It appears that there are at least three scopes for the `pyenv` configured
version of the `python` command:
* global - I believe this is a permanent, global setting
* local - sets up a config file in the project directory
* shell - the version is active just for the lifetime of the shell

I tried this for the shell scope and was able to run `gsutil`:
```shell
arthurryman@ArthursacStudio ~ % pyenv shell
pyenv: no shell-specific version configured
arthurryman@ArthursacStudio ~ % pyenv shell 3.12.11
arthurryman@ArthursacStudio ~ % pyenv shell
3.12.11
arthurryman@ArthursacStudio ~ % python --version
Python 3.12.11
arthurryman@ArthursacStudio ~ % gsutil config -n
This command will create a boto config file at
/Users/arthurryman/.boto containing your credentials, based on your
responses to the following questions.

Boto config file "/Users/arthurryman/.boto" created. If you need to
use a proxy to access the Internet please see the instructions in that
file.
arthurryman@ArthursacStudio ~ % python --version
Python 3.12.11
```

The `.boto` file was created:
```shell
% cat .boto 
# This file contains credentials and other configuration information needed
# by the boto library, used by gsutil. You can edit this file (e.g., to add
# credentials) but be careful not to mis-edit any of the variable names (like
# "gs_access_key_id") or remove important markers (like the "[Credentials]" and
# "[Boto]" section delimiters).
#
# This file was created by gsutil version 5.34 at 2025-07-01 14:25:45.
#
# You can create additional configuration files by running
# gsutil config [options] [-o <config-file>]


[Credentials]

# Google OAuth2 credentials are managed by the Cloud SDK and
# do not need to be present in this file.
# To add HMAC aws credentials for "s3://" URIs, edit and uncomment the
# following two lines:
#aws_access_key_id = <your aws access key ID>
#aws_secret_access_key = <your aws secret access key>
# The ability to specify an alternate storage host and port
# is primarily for cloud storage service developers.
# Setting a non-default gs_host only works if prefer_api=xml.
#s3_host = <alternate storage host address>
#s3_port = <alternate storage host port>
# In some cases, (e.g. VPC requests) the "host" HTTP header should
# be different than the host used in the request URL.
#s3_host_header = <alternate storage host header>
# To add HMAC google credentials for "gs://" URIs, edit and uncomment the
# following two lines:
#gs_access_key_id = <your google access key ID>
#gs_secret_access_key = <your google secret access key>
# The ability to specify an alternate storage host and port
# is primarily for cloud storage service developers.
# Setting a non-default gs_host only works if prefer_api=xml.
#gs_host = <alternate storage host address>
#gs_port = <alternate storage host port>
# In some cases, (e.g. VPC requests) the "host" HTTP header should
# be different than the host used in the request URL.
#gs_host_header = <alternate storage host header>
#gs_json_host = <alternate JSON API storage host address>
#gs_json_port = <alternate JSON API storage host port>
#gs_json_host_header = <alternate JSON API storage host header>

# To impersonate a service account for "%s://" URIs over
# JSON API, edit and uncomment the following line:
#%s_impersonate_service_account = <service account email>

# This configuration setting enables or disables mutual TLS
# authentication. The default value for this setting is "false". When
# set to "true", gsutil uses the configured client certificate as
# transport credential to access the APIs. The use of mTLS ensures that
# the access originates from a trusted enterprise device. When enabled,
# the client certificate is auto discovered using the endpoint
# verification agent. When set to "true" but no client certificate or
# key is found, users receive an error.
#use_client_certificate = False

# The command line to execute, which prints the
# certificate, private key, or password to use in
# conjunction with "use_client_certificate = True".
#cert_provider_command = <Absolute path to command to run for
#                         certification. Ex: "/scripts/gen_cert.sh">


[Boto]

# http_socket_timeout specifies the timeout (in seconds) used to tell httplib
# how long to wait for socket timeouts. The default is 70 seconds. Note that
# this timeout only applies to httplib, not to httplib2 (which is used for
# OAuth2 refresh/access token exchanges).
#http_socket_timeout = 70

# The following two options control the use of a secure transport for requests
# to S3 and Google Cloud Storage. It is highly recommended to set both options
# to True in production environments, especially when using OAuth2 bearer token
# authentication with Google Cloud Storage.

# Set 'https_validate_certificates' to False to disable server certificate
# checking. The default for this option in the boto library is currently
# 'False' (to avoid breaking apps that depend on invalid certificates); it is
# therefore strongly recommended to always set this option explicitly to True
# in configuration files, to protect against "man-in-the-middle" attacks.
https_validate_certificates = True

# 'debug' controls the level of debug messages printed for the XML API only:
# 0 for none, 1 for basic boto debug, 2 for all boto debug plus HTTP
# requests/responses.
#debug = <0, 1, or 2>

# 'num_retries' controls the number of retry attempts made when errors occur
# during data transfers. The default is 6.
# Note 1: You can cause gsutil to retry failures effectively infinitely by
# setting this value to a large number (like 10000). Doing that could be useful
# in cases where your network connection occasionally fails and is down for an
# extended period of time, because when it comes back up gsutil will continue
# retrying.  However, in general we recommend not setting the value above 10,
# because otherwise gsutil could appear to "hang" due to excessive retries
# (since unless you run gsutil -D you won't see any logged evidence that gsutil
# is retrying).
# Note 2: Don't set this value to 0, as it will cause boto to fail when reusing
# HTTP connections.
#num_retries = <integer value>

# 'max_retry_delay' controls the max delay (in seconds) between retries. The
# default value is 60, so the backoff sequence will be 1 seconds, 2 seconds, 4,
# 8, 16, 32, and then 60 for all subsequent retries for a given HTTP request.
# Note: At present this value only impacts the XML API and the JSON API uses a
# fixed value of 60.
#max_retry_delay = <integer value>

# To use a proxy, edit and uncomment the proxy and proxy_port lines.
# If you need a user/password with this proxy, edit and uncomment
# those lines as well. If your organization also disallows DNS
# lookups by client machines, set proxy_rdns to True (the default).
# If you have installed gsutil through the Cloud SDK and have 
# configured proxy settings in gcloud, those proxy settings will 
# override any other options (including those set here, along with 
# any settings in proxy-related environment variables). Otherwise, 
# if proxy_host and proxy_port are not specified in this file and
# one of the OS environment variables http_proxy, https_proxy, or
# HTTPS_PROXY is defined, gsutil will use the proxy server specified
# in these environment variables, in order of precedence according
# to how they are listed above.
#proxy = <proxy host>
#proxy_type = <proxy type (socks4, socks5, http) | Defaults to http>
#proxy_port = <proxy port>
#proxy_user = <proxy user>
#proxy_pass = <proxy password>
#proxy_rdns = <let proxy server perform DNS lookups (True,False); socks proxy not supported>

[GoogleCompute]

# 'service_account' specifies the a Google Compute Engine service account to
# use for credentials. This value is intended for use only on Google Compute
# Engine virtual machines and usually lives in /etc/boto.cfg. Most users
# shouldn't need to edit this part of the config.
#service_account = default

[GSUtil]

# 'resumable_threshold' specifies the smallest file size [bytes] for which
# resumable Google Cloud Storage uploads are attempted. The default is 8388608
# (8 MiB).
#resumable_threshold = 8388608

# 'rsync_buffer_lines' specifies the number of lines of bucket or directory
# listings saved in each temp file during sorting. (The complete set is
# split across temp files and separately sorted/merged, to avoid needing to
# fit everything in memory at once.) If you are trying to synchronize very
# large directories/buckets (e.g., containing millions or more objects),
# having too small a value here can cause gsutil to run out of open file
# handles. If that happens, you can try to increase the number of open file
# handles your system allows (e.g., see 'man ulimit' on Linux; see also
# http://docs.python.org/2/library/resource.html). If you can't do that (or
# if you're already at the upper limit), increasing rsync_buffer_lines will
# cause gsutil to use fewer file handles, but at the cost of more memory. With
# rsync_buffer_lines set to 32000 and assuming a typical URL is 100 bytes
# long, gsutil will require approximately 10 MiB of memory while building
# the synchronization state, and will require approximately 60 open file
# descriptors to build the synchronization state over all 1M source and 1M
# destination URLs. Memory and file descriptors are only consumed while
# building the state; once the state is built, it resides in two temp files that
# are read and processed incrementally during the actual copy/delete
# operations.
#rsync_buffer_lines = 32000

# 'state_dir' specifies the base location where files that
# need a static location are stored, such as pointers to credentials,
# resumable transfer tracker files, and the last software update check.
# By default these files are stored in ~/.gsutil
#state_dir = <file_path>
# gsutil periodically checks whether a new version of the gsutil software is
# available. 'software_update_check_period' specifies the number of days
# between such checks. The default is 30. Setting the value to 0 disables
# periodic software update checks.
#software_update_check_period = 30

# 'tab_completion_timeout' controls the timeout (in seconds) for tab
# completions that involve remote requests (such as bucket or object names).
# If tab completion does not succeed within this timeout, no tab completion
# suggestions will be returned.
# A value of 0 will disable completions that involve remote requests.
#tab_completion_timeout = 5

# 'parallel_process_count' and 'parallel_thread_count' specify the number
# of OS processes and Python threads, respectively, to use when executing
# operations in parallel. The default settings should work well as configured,
# however, to enhance performance for transfers involving large numbers of
# files, you may experiment with hand tuning these values to optimize
# performance for your particular system configuration.
#parallel_process_count = 12
#parallel_thread_count = 5

# 'parallel_composite_upload_threshold' specifies the maximum size of a file to
# upload in a single stream. Files larger than this threshold will be
# partitioned into component parts and uploaded in parallel and then composed
# into a single object.
# The number of components will be the smaller of
# ceil(file_size / parallel_composite_upload_component_size) and
# MAX_COMPOSE_ARITY. The current value of MAX_COMPOSE_ARITY is
# 32.
# If 'parallel_composite_upload_threshold' is set to 0, then automatic parallel
# uploads will never occur.
# Setting an extremely low threshold is unadvisable. The vast majority of
# environments will see degraded performance for thresholds below 80M, and it
# is almost never advantageous to have a threshold below 20M.
# 'parallel_composite_upload_component_size' specifies the ideal size of a
# component in bytes, which will act as an upper bound to the size of the
# components if ceil(file_size / parallel_composite_upload_component_size) is
# less than MAX_COMPOSE_ARITY.
# Values can be provided either in bytes or as human-readable values
# (e.g., "150M" to represent 150 mebibytes)
#
# Note: At present parallel composite uploads are disabled by default, because
# using composite objects requires a compiled crcmod (see "gsutil help crcmod"),
# and for operating systems that don't already have this package installed this
# makes gsutil harder to use. Google is actively working with a number of the
# Linux distributions to get crcmod included with the stock distribution. Once
# that is done we will re-enable parallel composite uploads by default in
# gsutil.
#
# Note: Parallel composite uploads should not be used with NEARLINE, COLDLINE,
# or ARCHIVE storage class buckets, as doing this incurs an early deletion
# charge for each component object.
#
# Note: Parallel composite uploads are not enabled with Cloud KMS encrypted
# objects as a source or destination, as composition with KMS objects is not yet
# supported.

#parallel_composite_upload_threshold = 0
#parallel_composite_upload_component_size = 50M

#
# 'parallel_composite_upload_bypass_kms_check' removes the object/bucket KMS checks
# used to guard composition of KMS objects.
#disable_parallel_composite_upload_kms_check = False

# 'sliced_object_download_threshold' and
# 'sliced_object_download_component_size' have analogous functionality to
# their respective parallel_composite_upload config values.
# 'sliced_object_download_max_components' specifies the maximum number of
# slices to be used when performing a sliced object download.
#sliced_object_download_threshold = 0
#sliced_object_download_component_size = 50M
#sliced_object_download_max_components = 4

# Compressed transport encoded uploads buffer chunks of compressed data. When
# running a composite upload and/or many uploads in parallel, compression may
# consume more memory than available. This setting restricts the number of
# compressed transport encoded uploads running in parallel such that they
# don't consume more memory than set here. This is 2GiB by default.
# Values can be provided either in bytes or as human-readable values
# (e.g., "2G" to represent 2 gibibytes)
#max_upload_compression_buffer_size = 2G

# GZIP compression level, if using compression. Reducing this can have
# a dramatic impact on compression speed with minor size increases.
# This is a value from 0-9, with 9 being max compression.
# A good level to try is 6, which is the default used by the gzip tool.
#gzip_compression_level = 9

# 'task_estimation_threshold' controls how many files or objects gsutil
# processes before it attempts to estimate the total work that will be
# performed by the command. Estimation makes extra directory listing or API
# list calls and is performed only if multiple processes and/or threads are
# used. Estimation can slightly increase cost due to extra
# listing calls; to disable it entirely, set this value to 0.
#task_estimation_threshold=30000

# 'use_magicfile' specifies if the 'file --mime <filename>' command should be
# used to guess content types instead of the default filename extension-based
# mechanism. Available on UNIX and macOS (and possibly on Windows, if you're
# running Cygwin or some other package that provides implementations of
# UNIX-like commands). When available and enabled use_magicfile should be more
# robust because it analyzes file contents in addition to extensions.
#use_magicfile = False

# Service account emails for testing the hmac command. If these fields are not
# populated with distinct service accounts the tests for the hmac command will
# not be run.  Primarily useful for tool developers.
#test_hmac_service_account =
#test_hmac_alt_service_account =
#test_hmac_list_service_account =

# Service account emails for testing impersonation credentials. If this field is
# not populated with a service account the tests for service account
# impersonation will not run.  Primarily useful for tool developers.
#test_impersonate_service_account =

# 'content_language' specifies the ISO 639-1 language code of the content, to be
# passed in the Content-Language header. By default no Content-Language is sent.
# See the ISO 639-1 column of
# http://www.loc.gov/standards/iso639-2/php/code_list.php for a list of
# language codes.
content_language = en

# 'check_hashes' specifies how strictly to require integrity checking for
# downloaded data. Legal values are:
#   'if_fast_else_fail' - (default) Only integrity check if the digest
#       will run efficiently (using compiled code), else fail the download.
#   'if_fast_else_skip' - Only integrity check if the server supplies a
#       hash and the local digest computation will run quickly, else skip the
#       check.
#   'always' - Always check download integrity regardless of possible
#       performance costs.
#   'never' - Don't perform download integrity checks. This setting is
#       not recommended except for special cases such as measuring download
#       performance excluding time for integrity checking.
# This option exists to assist users who wish to download a GCS composite object
# and are unable to install crcmod with the C-extension. CRC32c is the only
# available integrity check for composite objects, and without the C-extension,
# download performance can be significantly degraded by the digest computation.
# This option is ignored for daisy-chain copies, which don't compute hashes but
# instead (inexpensively) compare the cloud source and destination hashes.
#check_hashes = if_fast_else_fail

# 'encryption_key' specifies a single customer-supplied encryption key that
# will be used for all data written to Google Cloud Storage. See
# "gsutil help encryption" for more information
# Encryption key: RFC 4648 section 4 base64-encoded AES256 string
# Warning: If decrypt_key is specified without an encrypt_key, objects will be
# decrypted when copied in the cloud.
#encryption_key=

# Each 'decryption_key' entry specifies a customer-supplied decryption key that
# will be used to access and Google Cloud Storage objects encrypted with
# the corresponding key.
# Decryption keys: Up to 100 RFC 4648 section 4 base64-encoded AES256 strings
# in ascending numerical order, starting with 1.
#decryption_key1=
#decryption_key2=
#decryption_key3=

# The ability to specify an alternative JSON API version is primarily for cloud
# storage service developers.
#json_api_version = v1

# Specifies the API to use when interacting with cloud storage providers. If the
# gsutil command supports this API for the provider, it will be used instead of
# the default API. Commands typically default to XML for S3 and JSON for GCS.
# Note that if any encryption configuration options are set (see above), the
# JSON API will be used for interacting with Google Cloud Storage buckets even
# if XML is preferred, as gsutil does not currently support this functionality
# when using the XML API.
#prefer_api = json
#prefer_api = xml

# Disables the prompt asking for opt-in to data collection for analytics.
#disable_analytics_prompt = True

# The "test" command runs tests against regional buckets (unless you supply the
# `-b` option). By default, the region used is us-central1, but you can change
# the default region using this option.
#test_cmd_regional_bucket_location = us-central1

# Tests for the "notification watchbucket" command require a notification URL.
# If this option is not supplied, those tests will be skipped.
#test_notification_url = https://yourdomain.url/notification-endpoint

# Used in conjunction with --stet flag on cp command for end-to-end encryption.
# STET binary path. If not specified, gsutil checks PATH for "stet".
#stet_binary_path = <Path to binary "/usr/local/bin/stet">

# STET config path. If not specified, the STET binary will run with its default
# settings.
#stet_config_path = ~/.config/my_config.yaml

# Adds an API call before parallel operations that triggers a reauth challenge.
#trigger_reauth_challenge_for_parallel_operations = False


# 'default_api_version' specifies the default Google Cloud Storage XML API
# version to use. If not set below gsutil defaults to API version 1.
default_api_version = 2

[OAuth2]
# This section specifies options used with OAuth2 authentication.

# 'token_cache' specifies how the OAuth2 client should cache access tokens.
# Valid values are:
#  'in_memory': an in-memory cache is used. This is only useful if the boto
#      client instance (and with it the OAuth2 plugin instance) persists
#      across multiple requests.
#  'file_system' : access tokens will be cached in the file system, in files
#      whose names include a key derived from the refresh token the access token
#      based on.
# The default is 'file_system'.
#token_cache = file_system
#token_cache = in_memory

# 'token_cache_path_pattern' specifies a path pattern for token cache files.
# This option is only relevant if token_cache = file_system.
# The value of this option should be a path, with place-holders '%(key)s' (which
# will be replaced with a key derived from the refresh token the cached access
# token was based on), and (optionally), %(uid)s (which will be replaced with
# the UID of the current user, if available via os.getuid()).
# Note that the config parser itself interpolates '%' placeholders, and hence
# the above placeholders need to be escaped as '%%(key)s'.
# The default value of this option is
#  token_cache_path_pattern = <tmpdir>/oauth2client-tokencache.%%(uid)s.%%(key)s
# where <tmpdir> is the system-dependent default temp directory.

# The following options specify the label and endpoint URIs for the OAUth2
# authorization provider being used. Primarily useful for tool developers.
#provider_label = Google
#provider_authorization_uri = https://accounts.google.com/o/oauth2/auth
#provider_token_uri = https://oauth2.googleapis.com/token

# 'oauth2_refresh_retries' controls the number of retry attempts made when
# rate limiting errors occur for OAuth2 requests to retrieve an access token.
# The default value is 6.
#oauth2_refresh_retries = <integer value>

# The following options specify the OAuth2 client identity and secret that is
# used when requesting and using OAuth2 tokens. If not specified, a default
# OAuth2 client for the gsutil tool is used; for uses of the boto library (with
# OAuth2 authentication plugin) in other client software, it is recommended to
# use a tool/client-specific OAuth2 client. For more information on OAuth2, see
# http://code.google.com/apis/accounts/docs/OAuth2.html
#client_id = <OAuth2 client id>
#client_secret = <OAuth2 client secret>
```

Perhaps I don't need this file.

Now try using text-to-speech.

Previously, I got stuck in initializing the `gcloud` CLI because of
the Python version issue that affected the creation of `.boto`. 
Continue working through:
https://cloud.google.com/sdk/docs/initializing

List the config info:
```shell
 % gcloud config list
[core]
account = arthur.ryman@gmail.com
disable_usage_reporting = True
project = modern-mystery-464312-s3

Your active configuration is: [default]
```

Try to follow this guide:
https://cloud.google.com/text-to-speech/docs/create-audio-text-command-line

The prerequisite setup is described on:
https://cloud.google.com/text-to-speech/docs/before-you-begin

I created local authentication credentials by running:
```shell
gcloud auth application-default login
```
This opened a web browser on Google.
I assume it wrote credentials to some `gcloud` config file on
my machine.

```shell
% gcloud auth application-default login
Your browser has been opened to visit:

    https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8085%2F&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fsqlservice.login&state=wA8e96idpXYquVPjYbkuq5uxk39ChD&access_type=offline&code_challenge=XjrFhX8rYQfQG97WCTwNr-HUR-n1h0PWmsax6Oyysos&code_challenge_method=S256

You have consented to only few of the requested scopes, so some features may not work as expected. If you would like to give consent to all scopes, you can run the login command again. Requested scopes: ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/sqlservice.login'].
Scopes you consented for: ['https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/userinfo.email', 'openid'].
Missing scopes: ['https://www.googleapis.com/auth/sqlservice.login'].
Credentials saved to file: [/Users/arthurryman/.config/gcloud/application_default_credentials.json]

These credentials will be used by any library that requests Application Default Credentials (ADC).

Quota project "modern-mystery-464312-s3" was added to ADC which can be used by Google client libraries for billing and quota. Note that some services may still bill the project owning the resource.
```

Yes, the credentials are saved to `[/Users/arthurryman/.config/gcloud/application_default_credentials.json]`

There is also mention of an access token which can be obtained by running the command:
```shell
gcloud auth print-access-token
```

I assume that this access token is generated from the user credentials.
An access token usually is only valid for a limited time period.
It may be that the CLI handles generating it on a per-request basis.

Carry on at:
https://cloud.google.com/text-to-speech/docs/create-audio-text-command-line

This document describes how to make a REST request using curl.
It is rather awkward since you have to create the REST request file and
run it using `curl`, then grab the JSON output, extract the base64-encoded mp3
content, and finally decode it using the following command:
```shell
base64 --decode -i synthesize-output-base64.txt -o  synthesized-audio.mp3
```
However, this did all work, and it somewhat demystifies the mechanics of the
API.

More info on speech synthesis:
https://cloud.google.com/text-to-speech/docs/basics

Does the `gcloud` CLI make life simpler?
The answer is yes, but `gcloud` does not provide a subcommand to call the
text-to-speech service. However, it does provide subcommands for getting both
an access token and the project ID which are required for the REST request.

I created a shell script `speak.zsh` that converts text to mp3. 
It also sanitizes the text file by removing or replacing problematic characters.
For example, newlines caused artifacts in the mp3.
ChatGPT did a good job generating the zsh script.
Copy the script into the `voiceovers` directory and run the make from there.

Next, create a GNU makefile to automate the conversions.
Done.
I have converted all text files to mp3.
See the `speak.zsh` script and the `Makefile` in the `voiceovers` subdirectory.

## 2025-06-29

My goal is to run the Google text-to-speech service using the gcloud
CLI.

I installed the SDK which includes gcloud and some other commands.

Continue to read the docs.

Authentication next:
https://cloud.google.com/docs/authentication

Focus on:
```
Try out some gcloud commands in my local development environment.
```

https://cloud.google.com/docs/authentication/gcloud

Focus on local environment.

Try user credentials and `gcloud init`

```arthurryman@ArthursacStudio ~ % gcloud init
Welcome! This command will take you through the configuration of gcloud.

Your current configuration has been set to: [default]

You can skip diagnostics next time by using the following flag:
  gcloud init --skip-diagnostics

Network diagnostic detects and fixes local network connection issues.
Checking network connection...done.                                                                                                                                          
Reachability Check passed.
Network diagnostic passed (1/1 checks passed).

You must sign in to continue. Would you like to sign in (Y/n)?  Y

Your browser has been opened to visit:

    https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=32555940559.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8085%2F&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fappengine.admin+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fsqlservice.login+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcompute+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Faccounts.reauth&state=MKIrqJZIGlikskchixJzH8Rm1qJsgQ&access_type=offline&code_challenge=Mr64-e4X_gKzrBTVkBpcL0twZKon0BJrf2X2An9H3wE&code_challenge_method=S256

You are signed in as: [arthur.ryman@gmail.com].

Pick cloud project to use: 
 [1] modern-mystery-464312-s3
 [2] Enter a project ID
 [3] Create a new project
Please enter numeric choice or text value (must exactly match list item):  1

Your current project has been set to: [modern-mystery-464312-s3].

Not setting default zone/region (this feature makes it easier to use
[gcloud compute] by setting an appropriate default value for the
--zone and --region flag).
See https://cloud.google.com/compute/docs/gcloud-compute section on how to set
default compute region and zone manually. If you would like [gcloud init] to be
able to do this for you the next time you run it, make sure the
Compute Engine API is enabled for your project on the
https://console.developers.google.com/apis page.

Error creating a default .boto configuration file. Please run [gsutil config -n] if you would like to create this file.
The Google Cloud CLI is configured and ready to use!

* Commands that require authentication will use arthur.ryman@gmail.com by default
* Commands will reference project `modern-mystery-464312-s3` by default
Run `gcloud help config` to learn how to change individual settings

This gcloud configuration is called [default]. You can create additional configurations if you work with multiple accounts and/or projects.
Run `gcloud topic configurations` to learn more.

Some things to try next:

* Run `gcloud --help` to see the Cloud Platform services you can interact with. And run `gcloud help COMMAND` to get help on any gcloud command.
* Run `gcloud topic --help` to learn about advanced features of the CLI like arg files and output formatting
* Run `gcloud cheat-sheet` to see a roster of go-to `gcloud` commands.
```

The script reported an error creating the `.boto` file.
I run the following:

```% gsutil config -n
Error: gsutil requires Python version 3.8-3.12, but a different version is installed.
You are currently running Python 3.13
Follow the steps below to resolve this issue:
	1. Switch to Python 3.8-3.12 using your Python version manager or install an appropriate version.
	2. If you are unsure how to manage Python versions, visit [https://cloud.google.com/storage/docs/gsutil_install#specifications] for detailed instructions.
```
I am using Homebrew to manage my Python versions. 
My default is Python 3.13.
How can I make Python 3.12 the default?
Use the following:
```
brew unlink python@3.13
brew link python@3.12 --force --overwrite
```

That didn't work.
I reverted the change by relinking Python 3.13.
```brew link python@3.13```


## 2025-06-28

Will has been using the Google Cloud Platform (GCP)
Text-to-Speech (TTS) API to convert the voiceover text files
to MP3 audio files.
He checked in his Python code and a readme file.
I am going to do the tutorial.

I had to create a GCP account and project.
This involved confirming my credit card but Google already
had it on file for other purposes so nothing to worry about.

I created the account and received $415 in credits which expire
on 2025-09-27 when my free trail ends. 
I won't get charged anything unless I activate my full account.

If I do not activate my full account before the free trial ends,
then any resources that I created will be deleted.

Creating the free trial account also created a GCP project named
**My First Project**, Number: 475633063058, ID: modern-mystery-464312-s3.

https://console.cloud.google.com/welcome/new?project=modern-mystery-464312-s3&inv=1&invt=Ab1UuA

Google refers to the GCP website as the console.
I can access my project from there.

I went through the Google Cloud Console Tour.

I downloaded the gcloud CLI, but it looked like it was part of the
SDK, so I checked homebrew and found:

```
brew install --cask google-cloud-sdk
```

This installed Python 3.12 as a dependency. 
The installation looks successful:

```
arthurryman@ArthursacStudio google-cloud-sdk % which gcloud
/opt/homebrew/bin/gcloud
arthurryman@ArthursacStudio google-cloud-sdk % gcloud --version
Google Cloud SDK 528.0.0
bq 2.1.18
core 2025.06.20
gcloud-crc32c 1.0.0
gsutil 5.34
```