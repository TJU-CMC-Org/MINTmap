# helpers.py


def used_arguments_str(args):
    out = f"""'{args.input_file_path}'"""
    if args.custom_rpm is not None and args.custom_rpm > 0:
        out += f"""' --custom-rpm {args.custom_rpm}'"""
    out += f""" --mapping-bundle '{args.mapping_bundle_path}'"""
    out += f""" --prefix '{args.prefix}'"""
    return out
