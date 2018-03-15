import argparse
import requests

from snake_tail import command
from snake_tail import download
from snake_tail import file
from snake_tail import memory
from snake_tail import note
from snake_tail import scales
from snake_tail import store
from snake_tail import upload


requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member


def main():  # pylint: disable=too-many-locals, too-many-statements
    # NOTE: subparsers bug: https://bugs.python.org/issue9253#msg186387
    parser = argparse.ArgumentParser(prog='snake-tail')
    parser.add_argument('--insecure', action='store_true', help='ignore ssl verification')
    parser.add_argument('--json', action='store_true', help='return all output in json (where applicable)')

    subparsers = parser.add_subparsers(help='command help')
    subparsers.required = True
    subparsers.dest = 'snake_command'

    parser_command = subparsers.add_parser('command', help='execute a command on a sample in snake')
    parser_command.add_argument('scale', help='the scale the command belongs to')
    parser_command.add_argument('command', help='the command to execute on the sample')
    parser_command.add_argument('sha256_digest', help='the sha256 digest of the sample to execute the command on')
    parser_command.add_argument('--args', help='args for the command in json format (if supported)')
    parser_command.add_argument('-a', '--async', action='store_true', help='queue the command for asynchronous execution')
    parser_command.add_argument('-g', '--get', action='store_true', help='get an already executed command, rather than posting')
    parser_command.add_argument('-t', '--timeout', type=int, help='the maximum amount of time a command is allowed to execute for')

    # TODO: Support Commands
    # Commands placeholder

    parser_download = subparsers.add_parser('download', help='download a sample from snake')
    parser_download.add_argument('sha256_digest', help='the sha256 digest of the sample to download')
    parser_download.add_argument('-d', '--directory', metavar='FILE', help='where to save the file (default: pwd)')

    parser_file = subparsers.add_parser('file', help='get information about a file from snake')
    parser_file.add_argument('sha256_digest', help='the sha256 digest of the file to get information on')
    parser_file.add_argument('-d', '--delete', action='store_true', help='delete the file')
    parser_file.add_argument('-u', '--update', action='store_true', help='update the sample\'s metadata')
    parser_file.add_argument('--name', help='update the sample\'s name (-u must be used)')
    parser_file.add_argument('--description', help='update the sample\'s description (-u must be used)')
    parser_file.add_argument('--tags', help='update the sample\'s tags (-u must be used)')

    # TODO: Support files
    # Files placeholder

    parser_memory = subparsers.add_parser('memory', help='get information about a memory from snake')
    parser_memory.add_argument('sha256_digest', help='the sha256 digest of the memory to get information on')
    parser_memory.add_argument('-d', '--delete', action='store_true', help='delete the sample')
    parser_memory.add_argument('-u', '--update', action='store_true', help='update the sample\'s metadata')
    parser_memory.add_argument('--name', help='update the sample\'s name (-u must be used)')
    parser_memory.add_argument('--description', help='update the sample\'s description (-u must be used)')
    parser_memory.add_argument('--tags', help='update the sample\'s tags (-u must be used)')

    # TODO: Support memories
    # Memories placeholder

    parser_note = subparsers.add_parser('note', help='get the note for a sample')
    parser_note.add_argument('sha256_digest', help='the sha256 digest of the sample the note belongs to')
    parser_note.add_argument('-c', '--create', action='store_true', help='create the note')
    parser_note.add_argument('-d', '--delete', action='store_true', help='delete the note')
    parser_note.add_argument('-u', '--update', action='store_true', help='update the note')
    parser_note.add_argument('--body', help='the body of the note (use with -c or -u)')

    # TODO: Support notes
    # Notes placeholder

    parser_scale = subparsers.add_parser('scale', help='interact with snake\'s scales')
    parser_scale.add_argument('scale', help='the scale to interact with')
    scale_subparsers = parser_scale.add_subparsers(help='command help')
    scale_subparsers.required = True
    scale_subparsers.dest = 'scale_command'
    parser_scale_info = scale_subparsers.add_parser('info', help='get information about a scale')
    parser_scale_info.add_argument('-r', '--reload', action='store_false', help='ask snake to reload the scale')
    parser_scale_interface = scale_subparsers.add_parser('interface', help='interact with a service using a scale\'s interface component')
    parser_scale_interface.add_argument('command', help='the command to execute on the sample using the interface')
    parser_scale_interface.add_argument('sha256_digest', help='the sha256 digest of the sample')
    parser_scale_interface.add_argument('--args', help='args for the command in json format (if supported)')
    parser_scale_interface.add_argument('-t', '--type', help='the type of the command in the interface, pull or push (default: pull)')
    parser_scale_upload = scale_subparsers.add_parser('upload', help='upload a sample using a scale\'s upload component')
    parser_scale_upload.add_argument('args', help='args for the upload command in json format')
    parser_scale_upload.add_argument('--name', help='set name for sample (default: autoname)')
    parser_scale_upload.add_argument('--description', help='set description for sample')
    parser_scale_upload.add_argument('--tags', help='set tags for sample (comma separated)')
    parser_scale_upload.add_argument('--extract', action='store_true', help='extract the sample, must be zipped (default: false)')
    parser_scale_upload.add_argument('--password', help='password for extraction if zip is protected (default: none)')

    parser_scales = subparsers.add_parser('scales', help='list installed scales')
    parser_scales.add_argument('-r', '--reload', action='store_false', help='ask snake to reload the scales')

    parser_samples = subparsers.add_parser('store', help='get information about samples in snake')
    parser_samples.add_argument('-f', '--file-type', help='restrict results to a file type (file or memory)')
    parser_samples.add_argument('-l', '--limit', type=int, help='number of samples to retrieve')
    parser_samples.add_argument('--filter', help='filter the results (e.g. {"name":"procdump"}')
    parser_samples.add_argument('--operator', help='operator to apply to sort filters (default: and)')
    parser_samples.add_argument('--order', type=int, help='order to return the samples (default: -1 [descending])')
    parser_samples.add_argument('--sort', help='field to sort on (default: none)')

    parser_upload = subparsers.add_parser('upload', help='upload a sample to snake')
    parser_upload.add_argument('type', help='the type of file to upload (file or memory)')
    parser_upload.add_argument('file', help='the file to upload')
    parser_upload.add_argument('--name', help='set name for sample (default: file name)')
    parser_upload.add_argument('--description', help='set description for sample')
    parser_upload.add_argument('--tags', help='set tags for sample (comma separated)')
    parser_upload.add_argument('--extract', action='store_true', help='extract the sample, must be zipped (default: false)')
    parser_upload.add_argument('--password', help='password for extraction if zip is protected (default: none)')

    args = parser.parse_args()

    verify = not args.insecure

    if args.snake_command == 'command':
        command.command(args.scale, args.command, args.sha256_digest,
                        args=args.args,
                        asynchronous=args.async,
                        get=args.get,
                        timeout=args.timeout,
                        json=args.json,
                        verify=verify)
    elif args.snake_command == 'download':
        download.download(args.sha256_digest, args.directory, json=args.json, verify=verify)
    elif args.snake_command == 'file':
        file.file(args.sha256_digest,
                  delete=args.delete,
                  update=args.update,
                  name=args.name,
                  description=args.description,
                  tags=args.tags,
                  json=args.json,
                  verify=verify)
    elif args.snake_command == 'memory':
        memory.memory(args.sha256_digest,
                      delete=args.delete,
                      update=args.update,
                      name=args.name,
                      description=args.description,
                      tags=args.tags,
                      json=args.json,
                      verify=verify)
    elif args.snake_command == 'note':
        note.note(args.sha256_digest,
                  create=args.create,
                  delete=args.delete,
                  update=args.update,
                  body=args.body,
                  json=args.json,
                  verify=verify)
    elif args.snake_command == 'scale':
        if args.scale_command == 'info':
            scales.info(args.scale, args.reload, json=args.json, verify=verify)
        elif args.scale_command == 'interface':
            scales.interface(args.scale,
                             args.command,
                             args.sha256_digest,
                             args=args.args,
                             type=args.type,
                             json=args.json,
                             verify=verify)
        elif args.scale_command == 'upload':
            scales.upload(args.scale,
                          args.args,
                          name=args.name,
                          description=args.description,
                          tags=args.tags,
                          extract=args.extract,
                          password=args.password,
                          json=args.json,
                          verify=verify)
    elif args.snake_command == 'scales':
        scales.scales(args.reload, json=args.json, verify=verify)
    elif args.snake_command == 'store':
        store.samples(file_type=args.file_type,
                      limit=args.limit,
                      filter=args.filter,
                      operator=args.operator,
                      order=args.order,
                      sort=args.sort,
                      json=args.json,
                      verify=verify)
    elif args.snake_command == 'upload':
        upload.upload(args.type,
                      args.file,
                      name=args.name,
                      description=args.description,
                      tags=args.tags,
                      extract=args.extract,
                      password=args.password,
                      json=args.json,
                      verify=verify)


if __name__ == "__main__":
    main()
