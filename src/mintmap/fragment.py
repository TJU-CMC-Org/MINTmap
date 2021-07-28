# rrf.py

from .common.helpers import csv, csv_html, tsv


class Fragment():
    __slots__ = [
        'end',
        'molecule',
        'region',
        #'secondary_region',
        #'secondary_region_id',
        'sequence',
        'start',
        'strand',
        'type',
    ]
    # yapf:disable
    valid_chromosome_names = {
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
        '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
        '23', '24', 'MT'
    }
    assembly = None
    # yapf:enable

    def __init__(
        self,
        sequence=None,
        #region=None,
        type=None,
        molecule=None,
        #secondary_region_id=None,
        strand=None,
        start=None,
        end=None,
        genomic_coordinates=None
    ):
        self.sequence = sequence
        #self.region = region
        self.type = type
        #self.secondary_region_id = secondary_region_id
        self.strand = strand
        self.start = start
        self.end = end
        self.molecule = molecule
        #self.secondary_region = self.molecule.region(secondary_region_id)

    def __repr__(self):
        return f"<Fragment {self.type} {self.start} {self.end}>"

    @property
    def chrom_name(self):
        return str(self.region.molecule.chromosome)

    @property
    def internal_start(self):
        if self.start < self.region.start:
            return self.start - self.region.start
        else:
            return self.start + 1 - self.region.start

    @property
    def internal_end(self):
        return self.end + 1 - self.region.start

    @property
    def genomic_start(self):
        if self.molecule.strand:
            return self.region.molecule.start \
                - self.region.molecule.padding_size \
                + self.start
        else:
            return self.region.molecule.end \
                + self.molecule.padding_size \
                - self.start \
                - self.sequence.length + 1

    @property
    def genomic_end(self):
        if self.molecule.strand:
            return self.region.molecule.start \
                - self.region.molecule.padding_size \
                + self.end
        else:
            return self.region.molecule.end \
                + self.molecule.padding_size \
                - self.start

    @property
    def global_start(self):
        if self.start < self.molecule.padding_size:
            return self.start - self.region.molecule.padding_size
        else:
            return self.start + 1 - self.region.molecule.padding_size

    @property
    def global_end(self):
        return self.end + 1 - self.region.molecule.padding_size

    @property
    def genomic_strand_symbol(self):
        if self.strand and self.molecule.strand:
            return '+'
        elif not self.strand and self.molecule.strand:
            return '-'
        elif self.strand and not self.molecule.strand:
            return '-'
        elif not self.strand and not self.molecule.strand:
            return '+'

    @property
    def genomic_coordinates(self):
        if self.chrom_name in self.valid_chromosome_names:
            return '_'.join(
                [
                    self.chrom_name,
                    self.genomic_strand_symbol,
                    str(self.genomic_start),
                    str(self.genomic_end)
                ]
            )
        else:
            return 'na'

    @property
    def genome_browser_url(self):
        if self.chrom_name in self.valid_chromosome_names:
            return 'https://www.genome.ucsc.edu/cgi-bin/hgTracks' \
                + f"?db={self.assembly}" \
                + '&position=chr' \
                + ('M' if self.chrom_name == 'MT' else self.chrom_name) \
                + f":{self.genomic_start}-{self.genomic_end}"
        else:
            return None

    @property
    def genomic_coordinates_html(self):
        if self.chrom_name in self.valid_chromosome_names:
            return f"<a href={self.genome_browser_url}>" \
                + f"{self.genomic_coordinates}</a>"
        else:
            return 'na'

    @property
    def secondary_internal_start(self):
        if self.secondary_region:
            return self.start - self.secondary_region.start
        elif self.start in self.molecule.left_padding_range:
            return self.start + 1
        elif self.end in self.molecule.right_padding_range:
            return self.start - self.molecule.right_padding_range[0]
        else:
            return None

    @property
    def secondary_internal_end(self):
        if self.secondary_region:
            return self.end + 1 - self.secondary_region.start
        elif self.start in self.molecule.left_padding_range:
            return self.end + 1
        elif self.end in self.molecule.right_padding_range:
            return self.end + 1 - self.molecule.right_padding_range[0]
        else:
            return None

    @property
    def secondary_internal_range(self):
        if self.secondary_internal_start:
            return str(self.secondary_internal_start) \
                + ' to ' \
                + str(self.secondary_internal_end)
        else:
            return 'na'

    #@property
    #def type(self):
    #    if self.is_itrf:
    #        return 'i-trf'
    #    elif self.is_3trf:
    #        return '3-trf'
    #    elif self.is_5trf:
    #        return '5-trf'
    #    elif self.is_5utrf:
    #        return '5-u-trf'
    #    elif self.is_trf1s:
    #        return '5-u-trf'
    #    else:
    #        return 'drop'

    #@property
    #def is_trf1s(self):
    #    return self.start in self.molecule.range \
    #        and self.end in self.molecule.right_range

    #@property
    #def is_3trf(self):
    #    return self.end in self.molecule.end

    #@property
    #def is_itrf(self):
    #    return self.start in self.molecule.range \
    #        and self.end in self.molecule.range \
    #        and self.start != self.molecule.start \
    #        and self.end != self.molecule.end

    #@property
    #def is_5trf(self):
    #    return self.start == self.molecule.start

    #@property
    #def is_5utrf(self):
    #    #return self.start in self.molecule.range \
    #    #    and self.end in self.molecule.right_range
    #    return self.start in self.molecule.left_range \
    #        and self.end in self.molecule.range

    @classmethod
    def rrfs_to_txt(self, rrfs):
        return tsv(
            [
                # Genomic location and strand for rRF (hg38)
                csv(map(lambda i: i.genomic_coordinates,
                        rrfs)),
                # Parental RNA
                csv(map(lambda i: i.region.molecule.name,
                        rrfs)),
                # Internal range (parental RNA)
                csv(map(lambda i: f"{i.global_start} to {i.global_end}",
                        rrfs)),
                # Orientation with respect to Parental RNA
                csv(map(lambda i: 'sense' if i.strand else 'antisense',
                        rrfs)),
                # Parental region
                csv(map(lambda i: i.region.id,
                        rrfs)),
                # Internal range (parental region)
                csv(
                    map(
                        lambda i: f"{i.internal_start} to {i.internal_end}",
                        rrfs
                    )
                ),
                # Secondary region
                csv(map(lambda i: i.secondary_region_id or 'na',
                        rrfs)),
                # Internal range (secondary region)
                csv(map(lambda i: i.secondary_internal_range,
                        rrfs)),
                # rRF-type
                csv(map(lambda i: i.type,
                        rrfs)),
            ]
        )

    @classmethod
    def rrfs_to_html(self, rrfs):
        fields = [
            # Genomic location and strand for rRF (hg38)
            csv_html(map(lambda i: i.genomic_coordinates_html,
                         rrfs)),
            # Parental RNA
            csv_html(map(lambda i: i.region.molecule.name,
                         rrfs)),
            # Location within parental RNA
            csv_html(
                map(lambda i: f"{i.global_start} to {i.global_end}",
                    rrfs)
            ),
            # Orientation with respect to Parental RNA
            csv_html(map(lambda i: 'sense' if i.strand else 'antisense',
                         rrfs)),
            # Parental region
            csv_html(map(lambda i: i.region.id,
                         rrfs)),
            # Location within parental region
            csv_html(
                map(lambda i: f"{i.internal_start} to {i.internal_end}",
                    rrfs)
            ),
            # Secondary region
            csv_html(map(lambda i: i.secondary_region_id or 'na',
                         rrfs)),
            # Internal range (secondary region)
            csv_html(map(lambda i: i.secondary_internal_range,
                         rrfs)),
            # rRF-type
            csv_html(map(lambda i: i.type,
                         rrfs)),
        ]
        return ' '.join(map(lambda i: f"<td>{i}</td>", fields))
