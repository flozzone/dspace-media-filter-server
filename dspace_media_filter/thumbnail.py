from preview_generator.manager import PreviewManager

from dspace_media_filter.filter import MediaFilter, MediaFilterResponse, MediaFilterRequest


class ThumbnailFilterMediaRequest(MediaFilterRequest):
    def __init__(self, data):
        super().__init__(data)

        thumbnail_data = data.get('thumbnail', dict())
        self.width = thumbnail_data.get('width')
        self.height = thumbnail_data.get('height', 256)
        self.page = thumbnail_data.get('page', -1)


class FilterModule(MediaFilter):
    def __init__(self, cache_dir=None):
        super().__init__(cache_dir=cache_dir)
        self.manager = PreviewManager(cache_folder_path=self.cache_dir, create_folder=True)

    def filter(self, req: MediaFilterRequest) -> MediaFilterResponse:
        tn_req = ThumbnailFilterMediaRequest(req.data)
        result_file = self.manager.get_jpeg_preview(req.abs_file,
                                                    width=tn_req.width,
                                                    height=tn_req.height,
                                                    page=tn_req.page)
        return MediaFilterResponse(result_file_path=result_file)
