import AVFoundation
import CoreMedia
let a = CommandLine.arguments
let src = URL(fileURLWithPath: a[1]), dst = URL(fileURLWithPath: a[2])
let width = Int(a[3])!, height = Int(a[4])!, bitrate = Int(a[5])!
try? FileManager.default.removeItem(at: dst)
let asset = AVURLAsset(url: src)
let track = asset.tracks(withMediaType: .video)[0]
let comp = AVMutableVideoComposition()
comp.renderSize = CGSize(width: width, height: height)
comp.frameDuration = CMTime(value: 1, timescale: 30)
let inst = AVMutableVideoCompositionInstruction()
inst.timeRange = CMTimeRange(start: .zero, duration: asset.duration)
let li = AVMutableVideoCompositionLayerInstruction(assetTrack: track)
li.setTransform(CGAffineTransform(scaleX: CGFloat(width)/track.naturalSize.width, y: CGFloat(height)/track.naturalSize.height), at: .zero)
inst.layerInstructions = [li]
comp.instructions = [inst]
let reader = try AVAssetReader(asset: asset)
let out = AVAssetReaderVideoCompositionOutput(videoTracks: [track], videoSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA])
out.videoComposition = comp
reader.add(out)
let writer = try AVAssetWriter(outputURL: dst, fileType: .mp4)
let input = AVAssetWriterInput(mediaType: .video, outputSettings: [
  AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: width, AVVideoHeightKey: height,
  AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: bitrate, AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel, AVVideoMaxKeyFrameIntervalKey: 30]])
writer.add(input); writer.shouldOptimizeForNetworkUse = true
reader.startReading(); writer.startWriting(); writer.startSession(atSourceTime: .zero)
let q = DispatchQueue(label: "w")
let sem = DispatchSemaphore(value: 0)
input.requestMediaDataWhenReady(on: q) {
  while input.isReadyForMoreMediaData {
    if let s = out.copyNextSampleBuffer() { input.append(s) } else { input.markAsFinished(); writer.finishWriting { sem.signal() }; return }
  }
}
sem.wait()
print(writer.status.rawValue, writer.error as Any)
