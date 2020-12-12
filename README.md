# python_oodle
This is a simple python wrapper around my `liboodle` fork of [`ooz`](https://github.com/baconwaifu/ooz) that allows for python integration.
Note that this requires `liboodle` compiled and installed, it won't fetch it for you.

## Building
It's as easy as
```bash
python3 setup.py --user install
```
after you've installed the requisite `liboodle` (which is a bit more in-depth to build)

## Features
### "Primitive" API:

* Kraken_Decompress: Decompress Oodle Kraken streams.
* Kraken_Compress: Compress Oodle Kraken streams.
* Kraken_DecodeStep: A streaming Kraken decoder.

### "Pythonic" API:
* KrakenCompressionStream: Presents a file-like interface accepting either a file-like as output, or buffering to memory.
* KrakenDecompressStream: Same as above, but for decompression; Accepts a file-like as *input*. may support seeking (if the whole output is buffered)
Note: For Decompression, an output buffer of at least one window size is kept in memory. TODO: figure out the window size.
The Decompressor can also be fed compressed data, and decompress to a memory buffer if the input file-like is `None`, to support streaming *input* that can't be buffered directly.

Supported Algorithms:
* BitKnit
* Mermaid/Selkie
* Kraken/Hydra (LZQ1/Akkorokamui)
* Leviathan
* LZN
* LZB
* LZA
* LZH

## Implementation
`liboodle` usually does the heavy lifting of parsing the input blocks, however, it does expose enough 'primitive' functions in such a way that one can
potentially stream it data a block at a time, rather than needing to load the whole input into memory at once.

Given that oodle is mostly designed for decompressing straight to RAM, such as loading assets in video games, the memory pressure that
normally requires streaming *to disk* may or may not actually exist. 

### File-Likes
For the DecompressStream, whenever a read() occurs, it first checks it's "unconsumed" output buffer. if there's enough data to fulfil the request, it consumes them and returns them as a bytes-like.
If there is *not* enough data in the buffer to return, it will read from the source in 128KiB chunks, decompressing them until either EOF is hit, or enough data
to satisfy the read has been decoded. if EOF is hit, yet there is a 'partial' quantum (ie: one who's compressed length extends beyond the EOF) an EOFError is raised for the read.

The C implementation of DecodeStep *does not* consume any bytes from the buffer if it's too short to contain the full quantum. We either have to buffer input that isn't consumed,
or parse the quantum stream and "intelligently" size our reads to correspond exactly with the physical size of the block.

## Kraken Stream Format
Note: the stream format is independent of the compression type; all of them rely on 'quantum' chunks.
### Header
This is the stream header, or the first 2 bytes in the stream. Denotes compression type and stream-global flags.
`0x00`: the 'chunk flags' byte: ru00 0110. r is 'restart decoder' (?) and u is 'uncompressed stream' while the other bits are absolute (or 'usually seen as this', possibly checksum?)
`0x01`: the 'compression type' indicator: denotes the compression type. bit 7 (0x80) is the 'checksum blocks' flag.

### Quantum
A Kraken "Stream Quantum" or 'compressed chunk'. Contains exactly 256KiB when uncompressed (except if last block)
first 3 bytes are loaded as a big-endian u24, compressed size is & 0x3ffff (256k)
if the compressed size is less than 256k, two flags are at bits 18 and 19, and if checksumming is enabled, the next 3 bytes are loaded as a BE u24 value as well, which is the checksum.

if the size *is* 256k, and bit 18 is set, then the quantum is a 'whole-block match' and the next single byte is taken as a checksum.

## Roadmap
[] CPython wrapper for `liboodle`
[] Python Frontend
[] `liboodle` State Storage
[] Streaming Decompression
[] Streaming Compression
[] File-Like interfaces

## License
This wrapper is presented for use and distribution under the GNU GPLv3+ with an additional exception: It may be configured to link against the proprietary oodle library
to provide decompression support for formats that are either broken, or not implemented in the open-source component. Compression algorithms must be part of the open-source component.
